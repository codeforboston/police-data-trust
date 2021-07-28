import * as d3 from "d3"
import { Feature, Point } from "geojson"
import { useEffect, useRef, useState } from "react"
import useResizeObserver from "use-resize-observer"
import BaseMap from "./BaseMap"
import { MarkerDescription, MarkerLayer } from "./marker-layer"
import useData from "./useData"
import styles from "./map.module.css"

export type BoundingType = [[number, number], [number, number]]
export type D3CallableSelectionType = d3.Selection<Element, unknown, any, any>
export type D3ZoomEventType = d3.D3ZoomEvent<Element, any>
export type ZoomBehaviorType = d3.ZoomBehavior<Element, unknown>
export type DispatchType = d3.Dispatch<d3.ZoomTransform>

export default function Map() {
  const data = useData()
  const ref = useRef<HTMLDivElement>()
  const { width, height } = useResizeObserver({ ref })

  const zoomRef = useRef<SVGSVGElement>()

  const [markerParams, setMarkerParams] = useState<MarkerDescription[]>([])

  const zoom = d3.zoom().on("zoom", zoomed)
  const zoomContainer = d3.select("#zoom-container") as D3CallableSelectionType
  zoomContainer.call(zoom)

  function zoomed(event: D3ZoomEventType) {
    const { transform } = event
    zoomContainer.attr("transform", transform.toString())
  }

  const zoomResetButton = d3.select("#zoom-reset")
  zoomResetButton.on("click", (event: MouseEvent) => {
    zoomContainer.transition().duration(750).call(zoom.transform, d3.zoomIdentity)
  })

  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])

  const path = d3.geoPath(projection)

  useEffect(() => {
    if (!data) return

    const populationScale = d3
      .scaleLinear()
      .domain(d3.extent(data.features, (d) => d.properties.population))
      .range([1, 25])

    const getMarkerParamsFromFeature = (d: Feature) => {
      const markerParams: MarkerDescription = {
        geoCenter: projection((d.geometry as Point).coordinates as [number, number]),
        dataPoint: populationScale(d.properties.population),
        label: d.properties.city,
      }
      return markerParams
    }

    setMarkerParams(data.features.map((feature) => getMarkerParamsFromFeature(feature)))
  }, [data])

  const onMapClick = (event: MouseEvent) => {
    const target = event.target as any
    const d = target.__data__
    if (target.classList.contains("state")) {
      const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)

      event.stopPropagation()

      zoomContainer
        .transition()
        .duration(750)
        .call(
          zoom.transform,
          d3.zoomIdentity
            .translate(width / 2, height / 2)
            .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
            .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
          d3.pointer(event, zoomContainer.node())
        )
      data.filter.value = d.properties.name
      data.setFilterProperties({ ...data.filter })
    }
  }

  zoomContainer.on("click", onMapClick)

  return (
    <div
      id="map-container"
      className={styles.mapContainer}
      ref={ref}
      style={{ height: "80vh", width: "100vw" }}>
      <div
        className={styles.gridSettings}
        style={{ width: width, height: height, minHeight: height, minWidth: width }}>
        <div className={styles.svgWrapper}>
          <svg id="show-data" className={"showData"} viewBox={`0, 0, 1200, 700`}>
            <g ref={zoomRef} id="zoom-container">
              <rect className={styles.mapClickZone}></rect>
              <BaseMap projection={projection} />
              <MarkerLayer markersData={markerParams} />
            </g>
          </svg>
        </div>
        <div className={styles.mapButton}>
          <button className="primaryButton" id="zoom-reset">
            Reset Zoom
          </button>
        </div>
      </div>
    </div>
  )
}
