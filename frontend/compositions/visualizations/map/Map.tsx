import { select, zoom, zoomIdentity, ZoomTransform } from "d3"
import { geoAlbersUsa, geoPath } from "d3-geo"
import { Feature } from "geojson"
import React, { useCallback, useEffect, useMemo, useRef } from "react"
import useResizeObserver from "use-resize-observer"
import PopUp from "../popUps/popUpComp"
import { usePopUp } from "../popUps/popUps"
import {
  BoundingType,
  D3CallableSelectionType,
  D3ZoomEventType,
  PointCoord,
  TargetWithData
} from "../utilities/chartTypes"
import BaseMap from "./BaseMap"
import styles from "./map.module.css"
import MapKey from "./mapKey"
import { MarkerLayer } from "./marker-layer"
import { useBoundaryPaths } from "./useBoundaryPaths"
import useMarkerLayerSearchData from "./useMarkerLayerSearchData"

export default function Map() {
  const markersData = useMarkerLayerSearchData()

  const boundaryPaths = useBoundaryPaths()

  const { updatePopUp, popUpProps } = usePopUp()

  const mapRef = useRef<HTMLDivElement>()

  const zoomRef = useRef<ReturnType<typeof zoom>>()

  const projection = useMemo(() => {
    return geoAlbersUsa()
      .scale(1300)
      .translate([487.5 + 112, 305 + 50])
  }, [])

  const { width, height } = useResizeObserver({ ref: mapRef })

  const gZoomable = select("#zoom-container") as D3CallableSelectionType

  const path = useMemo(() => geoPath(projection), [projection])

  const calcFitFeatureToWindow = useCallback(
    (d: Feature) => {
      const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)
      const dWidth = x1 - x0
      const dHeight = y1 - y0
      const maxBound = Math.max(dWidth / width, dHeight / height)
      return zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1 / maxBound)
        .translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    },
    [height, path, width]
  )

  const moveMap = useCallback(
    (transform: ZoomTransform, transition = true, pointer?: PointCoord) => {
      const transformStr = transform.toString()
      if (transformStr.includes("NaN")) {
        return
      }
      transition
        ? gZoomable.transition().duration(100).attr("transform", transformStr)
        : gZoomable.transition().duration(5).attr("transform", transformStr)
    },
    [gZoomable]
  )

  const resetZoom = useCallback(() => {
    moveMap(zoomIdentity)
  }, [moveMap])

  const handleMapClick = useCallback(
    (event) => {
      event.stopPropagation()
      const target = event.target as TargetWithData
      const d = target.__data__ as Feature
      if (target.classList.contains("state")) {
        const clickTransform = calcFitFeatureToWindow(d) as ZoomTransform
        moveMap(clickTransform)
      }
    },
    [calcFitFeatureToWindow, moveMap]
  )

  const handleMapDoubleClick = useCallback(
    (event: MouseEvent) => {
      event.stopPropagation()
      event.stopImmediatePropagation()
      resetZoom()
    },
    [resetZoom]
  )

  const handleMouseMove = useCallback(
    (event: MouseEvent) => {
      const target = event.target as TargetWithData
      const mousePosition = { x: event.offsetX, y: event.offsetY }

      const isHovered = target.classList.contains("state")
      updatePopUp({
        hovered: isHovered,
        headerText: target.__data__?.properties.name,
        bodyText: `this is about ${target.__data__?.properties.name}`,
        location: mousePosition
      })
    },
    [updatePopUp]
  )

  const handleMouseOut = useCallback(
    (event: MouseEvent) => {
      const target = event.target as TargetWithData
      const isHovered = !target.classList.contains("state")
      updatePopUp({ hovered: isHovered })
    },
    [updatePopUp]
  )

  const zoomed = useCallback(
    (event: D3ZoomEventType) => {
      const { transform } = event
      moveMap(transform, false)
    },
    [moveMap]
  )

  useEffect(() => {
    if (!boundaryPaths) return
    zoomRef.current = zoom().on("zoom", zoomed)

    const svgElement = select("#map-svg") as D3CallableSelectionType
    svgElement.on("click", handleMapClick)
    svgElement.on("dblclick", handleMapDoubleClick)
    svgElement.on("mousemove", handleMouseMove)
    zoomRef.current && svgElement.call(zoomRef.current)

    const zoomResetButton = select("#zoom-reset")
    zoomResetButton.on("click", resetZoom)

    return () => {
      zoomResetButton.on("click", null)
      svgElement.on("click", null)
      svgElement.on("dblclick", null)
      svgElement.on("mousemove", null)
      zoomRef.current = null
    }
  }, [
    width,
    height,
    projection,
    resetZoom,
    calcFitFeatureToWindow,
    handleMapClick,
    moveMap,
    zoomed,
    handleMouseMove,
    boundaryPaths,
    handleMapDoubleClick,
    handleMouseOut
  ])

  return boundaryPaths ? (
    <div id="map-container" className={styles.mapContainer} ref={mapRef}>
      {/*ts-nocheck*/}
      <div id="map-wrapper" className={styles.mapWrapper}>
        <svg
          id="map-svg"
          role="img"
          aria-labelledby="title desc"
          className={styles.mapData}
          viewBox={`0, 0, 1200, 700`}>
          <title>US Map Graphic</title>
          <desc>A data graphic showing incidents of police violence by state.</desc>
          <g id="zoom-container">
            <BaseMap projection={projection} geoData={boundaryPaths} />
            <MarkerLayer markersData={[]} />
          </g>
        </svg>
        <PopUp {...popUpProps} />
        <MapKey title={"map-key"} />
        <div className={styles.mapButton}>
          <button className="primaryButton" id="zoom-reset">
            Reset Zoom
          </button>
        </div>
      </div>
    </div>
  ) : (
    <div ref={mapRef}>test container</div>
  )
}
