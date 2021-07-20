//@ts-nocheck
import { useEffect, useRef } from "react"
import BaseMap from "./BaseMap"
import useData from "./useData"
import * as d3 from "d3"
import useResizeObserver from "use-resize-observer"
import { circleMarker, MarkerLayer } from "../map-symbols"

export interface Map {}

export default function Map() {
  const data = useData()
  const ref = useRef()

  const dimensions = useResizeObserver({ ref })

  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])

  useEffect(() => {
    if (!data || !dimensions) return

    const { width, height } = dimensions

  }, [dimensions])

  return (
    <div id="map-background">
      <svg id="show-data" viewBox="0, 0, 1200, 700" ref={ref}>
        <MarkerLayer data={data} projection={projection}/>
        <BaseMap />
      </svg>
    </div>
  )
}
