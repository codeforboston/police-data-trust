//@ts-nocheck
import * as d3 from "d3"
import React, { useEffect, useRef, useState } from "react"
import * as topojson from "topojson"

export default function BaseMap() {
  const ref = useRef(null)
  // const projection = d3.geoIdentity().translate([-70, 42]).scale(4)
  const projection = d3
    .geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])
  const path = d3.geoPath().projection(projection)

  const [data, setData] = useState()

  // const link =
  // "https://cdn.freecodecamp.org/testable-projects-fcc/data/choropleth_map/counties.json"

  const link = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"

  const dataPromise = fetch(link)

  const opacityScale = d3.scaleLinear().domain([0, 50]).range([0, 1])

  useEffect(() => {
    dataPromise
      .then((res) => res.json())
      .then((data) => {

        const svg = d3.select(ref.current)

        svg
          .selectAll("path")
          .data(topojson.feature(data, data.objects.states).features)
          .enter()
          .append("path")
          .classed("map-geo-shape state", true)
          .attr("d", path)
          .attr("fill-opacity", (d) => opacityScale(d.id))
          .append("text")
          .text((d) => d.properties.name)
          .on("click", (e) => console.log(e.target))
      })
  }, [dataPromise])

  return <svg id="map" viewBox="0, 0, 1200, 700" ref={ref}></svg>
}
