import d3, {
  D3ZoomEvent,
  extent,
  pointer,
  scaleLinear,
  select,
  Selection,
  zoom,
  zoomIdentity,
  ZoomTransform
} from "d3"
import { geoAlbersUsa, geoPath } from "d3-geo"
import { Feature, Point } from "geojson"
import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import useResizeObserver from "use-resize-observer"
import BaseMap, { getFakeData } from "./BaseMap"
import styles from "./map.module.css"
import MapKey from "./mapKey"
import { MarkerDescription, MarkerLayer } from "./marker-layer"
import useData from "./useData"
import {
  PointCoord,
  BoundingType,
  D3CallableSelectionType,
  D3ZoomEventType
} from "../utilities/chartTypes"

export default function Map() {
  const data = useData()
  const mapRef = useRef<HTMLDivElement>()
  const zoomRef = useRef<ReturnType<typeof zoom>>()
  const { width, height } = useResizeObserver({ ref: mapRef })
  const [markerParams, setMarkerParams] = useState<MarkerDescription[]>([])

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
      const [x, y] = path.centroid(d)
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
      data.filter.value = null
      data.setFilterProperties({ ...data.filter })
    },
    [data, moveMap]
  )

  const getFeatureFromTarget = (target: any): Feature => target.__data__ as Feature

  const onMapClick = useCallback(
    (event: MouseEvent) => {
      event.stopPropagation()
      const target = event.target as any

      if (target.classList.contains("state")) {
        const d: Feature = getFeatureFromTarget(target)
        const clickTransform = calcFitFeatureToWindow(width, height, d) as ZoomTransform

        zoomRef.current?.transform(svgElement.transition(), clickTransform)

        data.filter.value = d.properties.name
        data.setFilterProperties({ ...data.filter })
      }
    },
    [calcFitFeatureToWindow, data, height, svgElement, width]
  )

  const zoomed = useCallback(
    (event: D3ZoomEventType) => {
      const { transform } = event
      moveMap(transform, false)
    },
    [moveMap]
  )

  useEffect(() => {
    zoomRef.current = zoom().on("zoom", zoomed)
    // const zoomZoom = zoomRef.current.on("zoom", zoomed)
    // svgElement.call(zoomZoom)
    svgElement.call(zoomRef.current)

    const zoomResetButton = select("#zoom-reset")
    zoomResetButton.on("click", resetZoom)
    svgElement.on("click", onMapClick)

    return () => {
      zoomResetButton.on(".click", null)
      // zoomZoom.on(".zoom", null)
      gZoomable.on(".click", null)
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
    onMapClick,
    moveMap,
    zoomed,
    gZoomable
  ])

  const valueScale = scaleLinear()
    .domain(extent(data.features as Feature[], (features: Feature) => features.properties.value))
    .range([1, 25])

  const getMarkerParamsFromFeature = useCallback(
    (d: Feature) => {
      const markerParams: MarkerDescription = {
        geoCenter: projection((d.geometry as Point).coordinates as PointCoord),
        dataPoint: valueScale(d.properties.value),
        label: d.properties.label
      }
      return markerParams
    },
    [valueScale, projection]
  )

  return (
    <div id="map-container" className={styles.mapContainer} ref={mapRef}>
      <div className={styles.mapWrapper}>
        <svg id="map-svg" className={styles.mapData} viewBox={`0, 0, 1200, 700`}>
          <g id="zoom-container">
            <BaseMap projection={projection} data={getFakeData()} />
            <MarkerLayer markersData={markerParams} />
          </g>
        </svg>
      </div>
      <div className={styles.mapButton}>
        <button className="primaryButton" id="zoom-reset">
          Reset Zoom
        </button>
      </div>
      <MapKey title={"map-key"} />
    </div>
  )
}
