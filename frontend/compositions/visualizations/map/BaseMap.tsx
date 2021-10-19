import * as d3 from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useEffect, useRef } from "react"
import * as topojson from "topojson-client"
import { presimplify, simplify } from "topojson-simplify"
import { Topology } from "topojson-specification"
import { PointCoord } from "../utilities/chartTypes"

// colors:
// --darkBlue: #303463;
// --lightBlue: #7caed7;
// --grey: #666666;
// --red: #bf1212;
// --linkBlue: #0645ad;
// --white: #ffffff;

type StateID = string

type FakeData = {
  UID: number
  location: PointCoord | StateID
  value: number
}
export interface BaseMapProps {
  projection: d3.GeoProjection
  data: FakeData[]
}

export const getFakeData = () => {
  let data: FakeData[] = [
    {
      UID: 1,
      location: "04",
      value: 10
    },
    {
      UID: 2,
      location: "05",
      value: 30
    },
    {
      UID: 3,
      location: "06",
      value: 100
    },
    {
      UID: 4,
      location: "09",
      value: 70
    },
    {
      UID: 5,
      location: "10",
      value: 20
    },
    {
      UID: 6,
      location: "11",
      value: 10
    },
    {
      UID: 7,
      location: "12",
      value: 30
    },
    {
      UID: 8,
      location: "13",
      value: 100
    },
    {
      UID: 9,
      location: "14",
      value: 70
    },
    {
      UID: 10,
      location: "15",
      value: 20
    }
  ]
  return data
}

export default function BaseMap(props: BaseMapProps) {
  const baseMapRef = useRef(null)
  const { projection, data } = props
  const link: string = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const stateOnlyLink = "https://cdn.jsdelivr.net/npm/us-atlas@3.0.0/states-10m.json"

  const dataPromise = fetch(stateOnlyLink)

  const path = d3.geoPath().projection(projection)

  const valueScale = d3.scaleLinear().domain([0, 100]).range([0, 1])
  const colorGradient = d3.interpolate("#7caed7", "#303463")

  useEffect(() => {
    if (!dataPromise) return
    dataPromise
      .then((res) => res.json())
      .then((topology: Topology) => {
        if (!topology) return
        // topology = presimplify(topology)

        const svg = d3.select(baseMapRef.current)

        // topology = simplify(topology, 0.05)

        const statesTopo = topojson.feature(topology, topology.objects.states) as FeatureCollection

        const defs = svg.append("defs")

        const erodeFilter = defs.append("filter").attr("id", "erode")

        erodeFilter
          .append("feMorphology")
          .attr("operator", "erode")
          .attr("result", "ERODE")
          .attr("radius", "3")

        const statePaths = defs
          .append("svg")
          .attr("id", "statePaths")
          .attr("width", "1200")
          .attr("height", "700")

        statePaths
          .selectAll("path")
          .data(statesTopo.features)
          .enter()
          .append("path")
          .attr("id", (d) => d.properties.name)
          .attr("d", path)
          .attr("fill", (d: Feature) => {
            const datum = data.find((i) => d.id === i.location)
            return datum ? colorGradient(valueScale(Number(datum.value))) : "#7caed7"
          })
          .attr("vector-effect", "non-scalling-stroke")
          .attr("filter", "url(#erode)")

        svg
          .append("use")
          .attr("href", "#statePaths")
          .attr("pointer-events", "all")
          .attr("cursor", "pointer")

        svg.append("use").attr("href", "#statePaths")
          .attr("stroke", "#66666")
          .attr("stroke-width", 2)
          .attr("stroke-join", "round")
          .attr("stroke-opacity", 1)
      })
  }, [data, dataPromise, valueScale, path, colorGradient])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}></svg>
}
