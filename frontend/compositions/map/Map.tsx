import * as d3 from "d3"
import { Feature, Point } from "geojson"
import { useEffect, useRef, useState } from "react"
import useResizeObserver from "use-resize-observer"
import BaseMap from "./BaseMap"
import styles from "./map.module.css"
import { MarkerDescription, MarkerLayer } from "./marker-layer"
import useData from "./useData"

export type BoundingType = [[number, number], [number, number]]
export type D3CallableSelectionType = d3.Selection<Element, unknown, any, any>
export type D3ZoomEventType = d3.D3ZoomEvent<Element, any>
export type ZoomBehaviorType = d3.ZoomBehavior<Element, unknown>
export type DispatchType = d3.Dispatch<d3.ZoomTransform>

export default function Map() {
  const data = useData()
  const mapRef = useRef<HTMLDivElement>()
  const zoomRef = useRef<SVGSVGElement>()
  const { width, height } = useResizeObserver({ ref: mapRef })
  const [markerParams, setMarkerParams] = useState<MarkerDescription[]>([])
  const [transform, setTransform] = useState<d3.ZoomTransform>(d3.zoomIdentity)

  useEffect(() => {
    const path = d3.geoPath(projection)

    const zoomMap = (zoomable: D3CallableSelectionType, transform: d3.ZoomTransform) => {
      console.log("zoomMap", transform)
      zoomable.transition().duration(750).call(zoom.transform, transform)
    }

    const svgZoomable = d3.select("#map-svg") as D3CallableSelectionType
    const zoom = d3.zoom().on("zoom", (event) => setTransform(event.transform))
    svgZoomable.call(zoom)

    /* 
    const gZoomable = d3.select("#zoom-container") as D3CallableSelectionType

    function zoomed(event: D3ZoomEventType) {
      const { transform } = event
      const transformStr = transform.toString()
      if (transformStr.includes("NaN")) return
      gZoomable.attr("transform", transformStr)
    }

    gZoomable.call(zoomIn)
*/
    const resetZoom = () => {
      zoomMap(svgZoomable, d3.zoomIdentity)
      // svgZoomable.transition().duration(750).call(zoom.transform, d3.zoomIdentity)
    }

    const zoomResetButton = d3.select("#zoom-reset")
    zoomResetButton.on("click", resetZoom)

    function onMapClick(event: MouseEvent){
      const target = event.target as any
      const d = target.__data__ as Feature
      event.stopPropagation()

      if (target.classList.contains("state")) {
        const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)

        const clickTransform = zoomIDFitToWindow(width, height, d)
        setTransform(clickTransform)

        console.log("mapClickZoom", path.bounds(d))
        console.log(zoomIDFitToWindow(width, height, d))

        /*         gZoomable
          .transition()
          .duration(750)
          .call(
            zoomIn.transform,
            d3.zoomIdentity
              .translate(width / 2, height / 2)
              .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
              .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
            d3.pointer(event, gZoomable.node())
          ) */
        data.filter.value = d.properties.name
        data.setFilterProperties({ ...data.filter })
      }
    }

    function zoomIDFitToWindow(width: number, height: number, d: Feature): d3.ZoomTransform {
      const [[x0, y0], [x1, y1]]: BoundingType = path.bounds(d)
      return d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
        .translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    }

    svgZoomable.on("click", onMapClick)

    return () => {
      zoomResetButton.on(".click", resetZoom)
      // zoom.on(".zoom", zoomed)
      svgZoomable.on(".click", onMapClick)
    }
  }, [])

  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])

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

  return (
    <div id="map-container" className={styles.mapContainer} ref={mapRef}>
      <div className={styles.gridSettings}>
        <div className={styles.mapWrapper}>
          <svg id="map-svg" className={styles.mapData} viewBox={`0, 0, 1200, 700`}>
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
