//@ts-nocheck
import { useEffect, useRef } from "react"
import BaseMap from "./BaseMap"
import useData from "./useData"
import * as d3 from "d3"
import useResizeObserver from "use-resize-observer"

export default function Map() {
  const data = useData()
  const ref = useRef()

  const dimensions = useResizeObserver({ ref })

  useEffect(() => {
    if (!data || !dimensions) return

    data.setFilterProperties("density", 500)

    console.log("data", data.data)
    console.log("dimensions", dimensions)

    const { width, height } = dimensions

    const projection = d3.geoMercator().rotate([0, -130]).center([40, 0]).scale(4)

    d3.select(ref.current)
      .selectAll("circle")
      .data(data.data.features)
      .enter()
      .append("circle")
      .attr("z-index", -10)
      .attr("r", 5)
      .attr("cx", (d) => projection(d.geometry.coordinates)[0])
      .attr("cy", (d) => d.geometry.coordinates[1])
      .attr("fill", "orange")
      .attr("pointer-events", "all")
      .attr("cursor", "pointer")
      .on("click", function (e) {
        console.log("circle", d.properties.city)
      })

    d3.select(ref.current)
      .append("rect")
      .classed("background", true)
      .attr("height", "100%")
      .attr("width", "100%")
      .attr("z-index", 10)
      .attr("fill", "transparent")
      .attr("stroke", "lightgray")
      .attr("stroke-width", "2px")
  }, [dimensions])

  return (
    <div>
      <svg id="showData" viewBox="0, 0, 900, 600" height="600" weight="900" ref={ref}>
        <BaseMap />
      </svg>
    </div>
  )
}
