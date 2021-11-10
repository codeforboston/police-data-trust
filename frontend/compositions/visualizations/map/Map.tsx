import { select, selectAll, zoom, zoomIdentity, ZoomTransform } from "d3"
import { geoAlbersUsa, geoPath } from "d3-geo"
import { Feature } from "geojson"
import { useCallback, useEffect, useMemo, useRef } from "react"
import useResizeObserver from "use-resize-observer"
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
import useData from "./useData"

export default function Map() {
  const data = useData()
  const mapRef = useRef<HTMLDivElement>()
  const zoomRef = useRef<ReturnType<typeof zoom>>()
  const { width, height } = useResizeObserver({ ref: mapRef })

  const projection = useMemo(() => {
    return geoAlbersUsa()
      .scale(1300)
      .translate([487.5 + 112, 305 + 50])
  }, [])

  const path = useMemo(() => geoPath(projection), [projection])

  const svgElement = select("#map-svg") as D3CallableSelectionType
  const gZoomable = select("#zoom-container") as D3CallableSelectionType

  const calcFitFeatureToWindow = useCallback(
    (width: number, height: number, d: Feature) => {
      const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)
      const dWidth = x1 - x0
      const dHeight = y1 - y0
      const maxBound = Math.max(dWidth / width, dHeight / height)
      return zoomIdentity
        .translate(width / 2, height / 2)
        .scale(1 / maxBound)
        .translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    },
    [path]
  )

  const moveMap = useCallback(
    (transform: ZoomTransform, transition = true, pointer?: PointCoord) => {
      const transformStr = transform.toString()
      if (transformStr.includes("NaN")) return
      transition
        ? gZoomable.transition().duration(500).attr("transform", transformStr)
        : gZoomable.transition().duration(10).attr("transform", transformStr)
    },
    [gZoomable]
  )

  const resetZoom = useCallback(
    (action: (transform: ZoomTransform, transition?: Boolean, pointer?: PointCoord) => void) => {
      const transform = zoomIdentity
      moveMap(transform)
    },
    [moveMap]
  )

  const handleMapClick = useCallback(
    (event) => {
      event.stopPropagation()
      const target = event.target as TargetWithData
      const d = target.__data__
      if (target.classList.contains("state")) {
        const clickTransform = calcFitFeatureToWindow(width, height, d) as ZoomTransform
        zoomRef.current?.transform(svgElement.transition(), clickTransform)
      }
    },
    [calcFitFeatureToWindow, height, svgElement, width]
  )

  const addToolTip = useCallback(() => {
    const tooltip = select("#map-wrapper")
      .append("div")
      .classed(styles.tooltipDiv, true)
      .classed("tooltip-div", true)
      .style("visibility", "hidden")

    tooltip.append("p").classed(styles.tooltipText, true).classed("tooltip-text", true)
  }, [])

  const handleMouseEnter = useCallback(() => {
    addToolTip()
  }, [addToolTip])

  const handleMouseMove = useCallback(
    (event: MouseEvent) => {
      const target = event.target as TargetWithData
      const d = target.__data__

      if (target.classList.contains("state") && select(".tooltip")) {
        const stateData = data.filter((i) => d.id === i.state)
        const value = stateData ? stateData.length : "no value"

        const tooltipPos = {
          x: event.offsetX,
          y: event.offsetY
        }

        select(".tooltip-text").html(`${d.properties.name} <br>
          incidents: ${value} <br>
          types of violence: ${
            stateData && stateData.map((d) => d.useOfForce.join(", ")).join(", ")
          } <br>  `)

        select(".tooltip-div")
          .style("transform", `translate(${tooltipPos.x}px, ${tooltipPos.y}px)`)
          .style("visibility", "visible")
      } else {
        select(".tooltip-div").style("visibility", "hidden")
      }
    },
    [data]
  )

  const handleMouseOut = useCallback((event: MouseEvent) => {
    selectAll(".tooltip-div").remove()
  }, [])

  const zoomed = useCallback(
    (event: D3ZoomEventType) => {
      const { transform } = event
      moveMap(transform, false)
    },
    [moveMap]
  )

  useEffect(() => {
    if (!data) return
    zoomRef.current = zoom().on("zoom", zoomed)
    svgElement.call(zoomRef.current)

    const zoomResetButton = select("#zoom-reset")
    zoomResetButton.on("click", resetZoom)

    svgElement.on("click", handleMapClick)

    svgElement.on("mouseenter", handleMouseEnter)
    svgElement.on("mousemove", handleMouseMove)
    svgElement.on("mouseleave", handleMouseOut)

    return () => {
      zoomResetButton.on("click", null)
      gZoomable.on("click", null)
      svgElement.on("click", null)
      zoomRef.current = null
    }
  }, [
    width,
    height,
    projection,
    data,
    resetZoom,
    calcFitFeatureToWindow,
    svgElement,
    handleMapClick,
    moveMap,
    zoomed,
    gZoomable,
    handleMouseMove,
    handleMouseOut,
    handleMouseEnter
  ])

  return data ? (
    <div id="map-container" className={styles.mapContainer} ref={mapRef}>
      <div id="map-wrapper" className={styles.mapWrapper}>
        <svg
          id="map-svg"
          role="img"
          aria-labelledby="title desc"
          className={styles.mapData}
          viewBox={`0, 0, 1200, 700`}>
          <title>US Map Graphic</title>
          <desc>A data graphic showing incidents of poice violence by state.</desc>
          <g id="zoom-container">
            <BaseMap projection={projection} data={data} />
          </g>
        </svg>
        <MapKey title={"map-key"} />
        <div className={styles.mapButton}>
          <button className="primaryButton" id="zoom-reset">
            Reset Zoom
          </button>
        </div>
      </div>
    </div>
  ) : (
    <div></div>
  )
}
