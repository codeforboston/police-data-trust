import * as d3 from "d3"
import { geoPath } from "d3-geo"
import { Feature, Point } from "geojson"
import { useEffect, useRef, useState } from "react"
import useResizeObserver from "use-resize-observer"
import BaseMap from "./BaseMap"
import { MarkerDescription, MarkerLayer } from "./marker-layer"
import useData from "./useData"

export type BoundingType = [[number, number], [number, number]]
export type D3CallableSelectionType = d3.Selection<Element, unknown, any, any>
export type D3ZoomEventType = d3.D3ZoomEvent<Element, any>
export type ZoomBehavior = d3.ZoomBehavior<Element, unknown>
export type DispatchType = d3.Dispatch<d3.ZoomTransform>

export default function Map() {
  const data = useData()
  const ref = useRef<HTMLDivElement>()
  const { width, height } = useResizeObserver({ ref })

  const zoomRef = useRef<SVGSVGElement>()

  const [markerParams, setMarkerParams] = useState<MarkerDescription[]>([])
  const [shouldShowCities, setShouldShowCities] = useState<boolean>(false)
  const [selectedState, setSelectedState] = useState<string | null>(null)

  // setting up map movements
  const zoom = d3.zoom().on("zoom", zoomed)
  const zoomContainer = d3.select(".zoom-container") as D3CallableSelectionType
  zoomContainer.call(zoom)

  function zoomed(event: D3ZoomEventType) {
    const { transform } = event
    zoomContainer.attr("transform", transform.toString())
  }

  const zoomResetButton = d3.select("#zoom-reset")
  zoomResetButton.on("click", (event: MouseEvent) => {
    setSelectedState(null)
    zoomContainer.transition().duration(750).call(zoom.transform, d3.zoomIdentity)
  })

  // projection calculates screen position from geographic coordinates
  // settings for the projection come from the baselayer data set
  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])
  const path = geoPath(projection)

  // set marker
  useEffect(() => {
    if (!data) return

    // populationScale calculates display points from population data set
    const populationScale = d3
      .scaleLinear()
      .domain(d3.extent(data.features, (d) => d.properties.population))
      .range([1, 25])

    // geMarkerParams collects data & display settings for each marker
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

  // zooms in on state when clicked
  // must be a listener as doesn't seem like you can pass selections and/or behaviors down to components successfully

  const onStateListener = (event: MouseEvent) => {
    const target = event.target as any
    const d = target.__data__
    if (!target.classList.contains("state")) return

    const [[x0, y0], [x1, y1]] = path.bounds(d)
    event.stopPropagation()
    setSelectedState(d.id)

    // zooms state to fill viewport
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

    // filter marker data by state clicked
    data.filter.value = d.properties.name
    data.setFilterProperties({ ...data.filter })
  }
  zoomContainer.on("click", onStateListener)

  return (
    <div
      id="map-background"
      ref={ref}
      style={{
        gridColumn: "20% 60% 20%",
        height: "100vh",
        position: "relative",
      }}>
      <div className="map-button">
        <button className="primaryButton" id="zoom-reset">
          Reset Zoom
        </button>
      </div>
      <svg id="show-data" viewBox={`0, 0, 1200, 700`} width={width} height={height}>
        <g ref={zoomRef} className={"zoom-container"}>
          <BaseMap projection={projection} />
          <MarkerLayer markersData={markerParams} />
        </g>
      </svg>
    </div>
  )
}
