import * as d3 from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useEffect, useRef, useState } from "react"
import * as topojson from "topojson-client"
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

function useBoundaryPaths(): FeatureCollection {
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

    // Set the title after loading data to facilitate testing
    svg.attr("title", "US Map")

    /* Definitions */
    const defs = svg.append("defs")

    const strokeShape = defs.append("filter").attr("id", "strokeShape")

    strokeShape
      .append("feMorphology")
      .attr("operator", "erode")
      .attr("radius", 1)
      .attr("result", "erode")

    strokeShape
      .append("feGaussianBlur")
      .attr("in", "erode")
      .attr("stdDeviation", "3")
      .attr("result", "blurFilter")

    strokeShape
      .append("feColorMatrix")
      .attr("id", "colorMatrix2")
      .attr("in", "blurFilter")
      .attr("mode", "matrix")
      .attr("values", "1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 14 -7")
      .attr("result", "colorMatrix2")

    strokeShape
      .append("feGaussianBlur")
      .attr("in", "erode")
      .attr("stdDeviation", "2")
      .attr("result", "blurFilter2")

    strokeShape
      .append("feComposite")
      .attr("in", "colorMatrix2")
      .attr("in2", "blurFilter2")
      .attr("operator", "out")
      .attr("result", "compositedStroke")

    strokeShape
      .append("feBlend")
      .attr("in", "colorMatrix2")
      .attr("in2", "compositedStroke")
      .attr("mode", "multiply")

    const paths = svg.append("g").attr("id", "paths")
        /* SVG Body */
        paths
          .selectAll("path")
          .data(geoData.features)
          .enter()
          .append("path")
          .classed("state", true)
          .attr("title", (d) => d.properties.name)
          .attr("d", path)
          .attr("filter", "url(#strokeShape)")
          .attr("fill", (d: Feature) => {
            const countIncidents = data.filter((i) => d.id === i.state).length
            return colorGradient(valueScale(countIncidents))
          })
          .attr("pointer-events", "all")
          .attr("cursor", "pointer")

    return () => {
      defs.remove()
      paths.remove()
    }
  }, [data, valueScale, path, colorGradient, geoData, svg])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}></svg>
}
