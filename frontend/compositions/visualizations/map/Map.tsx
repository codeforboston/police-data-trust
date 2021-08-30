import {
  D3ZoomEvent,
  extent,
  pointer,
  scaleLinear,
  select,
  Selection,
  zoom,
  zoomIdentity,
  ZoomTransform,
} from "d3"
import { geoAlbersUsa, geoPath } from "d3-geo"
import { Feature, Point } from "geojson"
import { useEffect, useRef, useState } from "react"
import useResizeObserver from "use-resize-observer"
import BaseMap from "./BaseMap"
import styles from "./map.module.css"
import MapKey from "./mapKey"
import { MarkerDescription, MarkerLayer } from "./marker-layer"
import useData from "./useData"

export type Pair<T> = [T, T]
export type PointCoord = Pair<number>
export type BoundingType = [PointCoord, PointCoord]
export type D3CallableSelectionType = Selection<Element, unknown, any, any>
export type D3ZoomEventType = D3ZoomEvent<Element, any>

export default function Map() {
  const data = useData()
  const mapRef = useRef<HTMLDivElement>()
  const zoomRef = useRef<SVGSVGElement>()
  const { width, height } = useResizeObserver({ ref: mapRef })
  const [markerParams, setMarkerParams] = useState<MarkerDescription[]>([])
  const [focusedState, setFocusedState] = useState<D3CallableSelectionType | null>(null)

  useEffect(() => {
    const path = geoPath(projection)

    const svgElement = select("#map-svg") as D3CallableSelectionType
    const gZoomable = select("#zoom-container") as D3CallableSelectionType

    function zoomed(event: D3ZoomEventType) {
      const { transform } = event
      moveMap(transform, false)
    }

    const zoomZoom = zoom().on("zoom", zoomed)
    svgElement.call(zoomZoom)

    const zoomResetButton = select("#zoom-reset")

    const resetZoom = () => {
      const transform = zoomIdentity
      moveMap(transform)
      setFocusedState(null)

      data.filter.value = null
      data.setFilterProperties({ ...data.filter })
    }

    zoomResetButton.on("click", resetZoom)

    function moveMap(transform: ZoomTransform, transition = true, pointer?: PointCoord) {
      const transformStr = transform.toString()
      if (transformStr.includes("NaN")) return
      const mover = transition ? gZoomable.transition().duration(500) : gZoomable
      mover.attr("transform", transformStr)
    }

    const onMapClick = (event: MouseEvent) => {
      const target = event.target as any
      const d = target.__data__ as Feature
      event.stopPropagation()

      if (target.classList.contains("state")) {
        const clickTransform = calcFitFeatureToWindow(width, height, d)
        const d3Pointer = pointer(event, gZoomable.node())
        moveMap(clickTransform || zoomIdentity, true, d3Pointer)
        setFocusedState(d.properties.name)

        data.filter.value = d.properties.name
        data.setFilterProperties({ ...data.filter })
      }
    }

    svgElement.on("click", onMapClick)

    function calcFitFeatureToWindow(width: number, height: number, d: Feature): d3.ZoomTransform {
      const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)
      return zoomIdentity
        .translate(width / 2, height / 2)
        .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
        .translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    }

    return () => {
      zoomResetButton.on(".click", resetZoom)
      zoomZoom.on(".zoom", zoomed)
      svgElement.on(".click", onMapClick)
    }
  }, [width, height])

  const projection = geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])

  useEffect(() => {
    if (!data) return

    const populationScale = scaleLinear()
      .domain(extent((data.features as Feature[]), (features: Feature) => features.properties.population))
      .range([1, 25])

    const getMarkerParamsFromFeature = (d: Feature) => {
      const markerParams: MarkerDescription = {
        geoCenter: projection((d.geometry as Point).coordinates as [number, number]),
        dataPoint: populationScale(d.properties.population),
        label: d.properties.city
      }
      return markerParams
    }

    setMarkerParams(data.features.map((feature: Feature) => getMarkerParamsFromFeature(feature)))
  }, [data])

  return (
    <div id="map-container" className={styles.mapContainer} ref={mapRef}>
      <div className={styles.mapWrapper}>
        <svg id="map-svg" className={styles.mapData} viewBox={`0, 0, 1200, 700`}>
          <g ref={zoomRef} id="zoom-container">
            <BaseMap projection={projection} />
            <MarkerLayer markersData={markerParams} />
          </g>
        </svg>
        {focusedState}
      </div>
      <div className={styles.mapButton}>
        <button className="primaryButton" id="zoom-reset">
          Reset Zoom
        </button>
      </div>
      <MapKey title={"map-key"}/>
    </div>
  )
}
