import * as d3 from "d3"
import { FeatureCollection } from "geojson"
import React, { useEffect, useRef } from "react"
import * as topojson from "topojson"
import { Topology } from "topojson-specification"

type BaseMapProps = {
  projection: d3.GeoProjection
}

export default function BaseMap(props: BaseMapProps) {
  const ref = useRef(null)
  const { projection} = props

  // gets geojson data holding borders for us, states, and counties with names
  const link: string = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const dataPromise = fetch(link)

  // path is how you apply the projection to other data
  const path = d3.geoPath().projection(projection)

  const opacityScale = d3.scaleLinear().domain([0, 50]).range([0, 1])

  useEffect(() => {
    dataPromise
      .then((res) => res.json())
      .then((data: Topology) => {
        const svg = d3.select(ref.current).classed("map-geo-shape state", true)
        const statesTopo = topojson.feature(data, data.objects.states) as FeatureCollection
        svg
          .selectAll("path")
          .data(statesTopo.features)
          .enter()
          .append("path")
          .attr("id", (d) => d.properties.name)
          .classed("state", true)
          .attr("d", path)
          .attr("fill-opacity", (d) => opacityScale(Number(d.id)))
      })
  }, [dataPromise])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={ref}></svg>
}
