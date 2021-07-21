//@ts-nocheck
import * as d3 from "d3"
import React, { useEffect, useRef, useState } from "react"
import * as topojson from "topojson"

type BaseMapProps = {
  projection: d3.GeoProjection
}

export default function BaseMap(props: BaseMapProps) {
  const ref = useRef(null)
  const { projection } = props

  // gets geojson data holding borders for us, states, and counties with names
  const link: string = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const dataPromise = fetch(link)

  // path is how you apply the projection to other data
  const path = d3.geoPath().projection(projection)

  const opacityScale = d3.scaleLinear().domain([0, 50]).range([0, 1])

  function stateclick(d, e){
    console.log(d, e)
    
  }

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
          .on("click", (d) => stateclick(d))
      })
  }, [dataPromise])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={ref}></svg>
}
