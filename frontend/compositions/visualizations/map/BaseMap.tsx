import * as d3 from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react"
import * as topojson from "topojson-client"
import { simplify } from "topojson-simplify"
import { Topology } from "topojson-specification"
import { PointCoord } from "./Map"
import styles from "./map.module.css"

type StateID = number

type FakeData = {
  UID: string
  location: PointCoord | string | StateID
  value: number
}
export interface BaseMapProps {
  projection: d3.GeoProjection
  data: FakeData[]
}

export const getFakeData = () => {
  let data: FakeData[] = [
    {
      UID: "01",
      location: 4,
      value: 10
    },
    {
      UID: "02",
      location: 5,
      value: 30
    },
    {
      UID: "03",
      location: 6,
      value: 100
    },
    {
      UID: "04",
      location: 7,
      value: 70
    },
    {
      UID: "05",
      location: 8,
      value: 20
    }
  ]
  return data
}

export default function BaseMap(props: BaseMapProps) {
  const baseMapRef = useRef(null)
  const { projection, data } = props
  const link: string = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const dataPromise = fetch(link)

  const path = d3.geoPath().projection(projection)

  const opacityScale = d3.scaleLinear().domain([0, 50]).range([0, 1])

  useEffect(() => {
    if (!dataPromise) return
    dataPromise
      .then((res) => res.json())
      .then((topology: Topology) => {
        if (!topology) return
        const svg = d3
          .select(baseMapRef.current)
          .classed(styles.mapGeoShape, true)
          .classed(styles.state, true)
        const statesTopo = topojson.feature(topology, topology.objects.states) as FeatureCollection
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
  }, [data, dataPromise, opacityScale, path])

  return <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}></svg>
}
