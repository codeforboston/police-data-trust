//@ts-nocheck
import { useEffect, useRef } from "react"
import BaseMap from "./BaseMap"
import useData from "./useData"
import * as d3 from "d3"
import useResizeObserver from "use-resize-observer"

export interface Map {}

export default function Map() {
  const data = useData()
  const ref = useRef()

  const dimensions = useResizeObserver({ ref })

  const projection = d3.geoAlbersUsa().scale(1300).translate([487.5 + 112, 305 + 50])

  useEffect(() => {
    if (!data || !dimensions) return

    // console.log("data", data.data)
    // console.log("dimensions", dimensions)

    const { width, height } = dimensions
    // const coordinatesX = data.data.features.map((f) => f.geometry.coordinates[0])
    // const coordinatesY = data.data.features.map((f) => f.geometry.coordinates[1])

    // const maxPopX = d3.max(coordinatesX)
    // const minPopX = d3.min(coordinatesX)

    // const maxPopY = d3.max(coordinatesY)
    // const minPopY = d3.min(coordinatesY)

    // console.log(maxPopX, minPopX, maxPopY, minPopY)

    // const scaleX = d3.scaleLinear().domain(minPopX, maxPopX).range(0, width)
    // const scaleY = d3.scaleLinear().domain(minPopY, maxPopY).range(height, 0)


    const pCx = (coords) => {
      const pCoords = projection(coords)
      if (pCoords === null){
        return [0,0]
      }
      return pCoords[0]
    }

    const pCy = (coords) => {
      const pCoords = projection(coords)
      if (pCoords === null){
        return [0,0]
      }
      return pCoords[1]
    }

    const popSizeScale = d3.scaleLinear()
    .domain([100000, 5000000])
    .range([1, 8])

    const populationScale = d3.scaleLinear()
      .domain([100000, 50000000])
      .range([ "#7caed7", "#303463"])

    const opacityScale = d3.scaleLinear()
      .domain([0, 5000000])
      .range([0, 1])

    d3.select(ref.current)
      .selectAll("circle")
      .data(data.data.features.filter(f => f.properties.population > 100000))
      .enter()
      .append("circle")
      .classed("map-city-point map-population", true)
      .attr("z-index", -10)
      .attr("r", (d) => popSizeScale(d.properties.population))
      .attr("cx", (d) => pCx(d.geometry.coordinates))
      .attr("cy", (d) => pCy(d.geometry.coordinates))
      .attr("fill", (d) => populationScale(d.properties.population))
      .attr("fill-opacity", 0.8)
      .attr("pointer-events", "all")
      .attr("cursor", "pointer")
      .on("click", function (e) {
        d => console.log("circle", d.properties.city)
      })
      .append("text")
      .text(d => d.properties.city)

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
    <div id="map-background">
      <svg id="show-data" viewBox="0, 0, 1200, 700" ref={ref}>
        <BaseMap />
      </svg>
    </div>
  )
}
