//@ts-nocheck
import * as d3 from "d3"
import React, { useEffect, useRef, useState } from "react"
import * as topojson from "topojson"

export default function BaseMap() {
  const ref = useRef(null)
  const projection = d3.geoIdentity()
  const path = d3.geoPath().projection(projection)

  const [data, setData] = useState()

  const link =
    "https://cdn.freecodecamp.org/testable-projects-fcc/data/choropleth_map/counties.json"
  // const link = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"

  const dataPromise = fetch(link)

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
          .attr("d", path)
          .attr("fill", "white")
          .attr("stroke", "#639bc5")
          .attr("stroke-width", 1)
          
      })

  }, [dataPromise])

  return <svg id="map" viewBox="0, 0, 1200, 600" ref={ref}></svg>
}
