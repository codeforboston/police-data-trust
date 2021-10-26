import * as d3 from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useEffect, useRef, useState } from "react"
import * as topojson from "topojson-client"
import { topology } from "topojson-server"
import { presimplify, simplify } from "topojson-simplify"
import { Topology } from "topojson-specification"
import { FakeData } from "../utilities/chartTypes"

// colors:
// --darkBlue: #303463;
// --lightBlue: #7caed7;
// --grey: #666666;
// --red: #bf1212;
// --linkBlue: #0645ad;
// --white: #ffffff;

export interface BaseMapProps {
  projection: d3.GeoProjection
  data: FakeData[]
}

function useBoundaryPaths() {
  const wholeTopo = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const stateOnlyTopo = "https://cdn.jsdelivr.net/npm/us-atlas@3.0.0/states-10m.json"

  const [geoData, setGeoData] = useState<FeatureCollection>(null)

  useEffect(
    () =>
      void fetch(stateOnlyTopo)
        .then((res) => res.json())
        .then((topology?: Topology) => {
          if (!topology) return

          topology = presimplify(topology)
          topology = simplify(topology, 0.05)

          const statesTopo = topojson.feature(
            topology,
            topology.objects.states
          ) as FeatureCollection
          return statesTopo
        })
        .then(setGeoData),
    [setGeoData]
  )
  return geoData
}

export default function BaseMap(props: BaseMapProps) {
  const baseMapRef = useRef(null)
  const { projection, data } = props

  const geoData = useBoundaryPaths()

  const path = d3.geoPath().projection(projection)

  const valueScale = d3.scaleLinear().domain([0, 5]).range([0, 1])
  const colorGradient = d3.interpolate("#7caed7", "#303463")

  const svg = d3.select(baseMapRef.current)

  useEffect(() => {
    if (!geoData) return

    /* Definitions */
    const defs = svg.append("defs")

    const erodeFilter = defs.append("filter").attr("id", "erode")

    erodeFilter
      .append("feMorphology")
      .attr("operator", "erode")
      .attr("result", "ERODE")
      .attr("radius", "2")

    const statePaths = defs
      .append("svg")
      .attr("id", "statePaths")
      .attr("width", "1200")
      .attr("height", "700")

    statePaths
      .selectAll("path")
      .data(geoData.features)
      .enter()
      .append("path")
      .classed("state", true)
      .attr("id", (d) => d.properties.name)
      .attr("d", path)
      .attr("fill", "transparent")

    /* SVG Body */
    const paths = svg
      .append("g")
      .selectAll("path")
      .data(geoData.features)
      .enter()
      .append("path")
      .classed("state", true)
      .attr("title", (d) => d.id)
      .attr("d", path)
      .attr("fill", (d: Feature) => {
        const countIncidents = data.filter((i) => d.id === i.state).length
        return colorGradient(valueScale(countIncidents))
      })
      .attr("pointer-events", "all")
      .attr("cursor", "pointer")

    svg
      .append("use")
      .attr("id", "statePaths")
      .attr("href", "#statePaths")
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .attr("stroke-join", "round")
      .attr("stroke-opacity", 1)

    return () => {
      paths.remove()
      statePaths.remove()
    }
  }, [data, geoData, valueScale, path, colorGradient, svg])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}></svg>
}
