//@ts-nocheck
import { useEffect, useRef, useState } from "react"
import BaseMap from "./BaseMap"
import useData from "./useData"
import * as d3 from "d3"
import useResizeObserver from "use-resize-observer"
import { MarkerLayer } from "./marker-layer"

export interface Map {}

export default function Map() {
  const data = useData()
  const ref = useRef()

  const [translate, setTranslate] = useState<Coord>([487.5 + 112, 305 + 50])


  // we'll use projection to correctly overlay other geodata on the base map
  // type/scale/translate taken from the baselayer data set
  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    // .translate([487.5 + 112, 305 + 50])
    .translate(translate)


  return (
    <div
      ref={ref}
      id="map-background"
      style={{
        outline: "1px solid yellow",
        height: "100vh"
      }}>
      <svg id="show-data" viewBox={`0, 0, 1200, 700`}  height="100%" width="100%">
        <MarkerLayer data={data} projection={projection} />
        <BaseMap projection={projection}/>
      </svg>
    </div>
  )
}
