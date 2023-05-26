import { geoPath, scaleLinear, interpolate, select } from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useEffect, useRef, useState } from "react"

export interface BaseMapProps {
  projection: d3.GeoProjection
  geoData: FeatureCollection
}

export default function BaseMap(props: BaseMapProps) {
  const baseMapRef = useRef(null)
  const { projection, geoData } = props
  const [reload, setReload] = useState(1)
  const path = geoPath().projection(projection)

  const valueScale = scaleLinear().domain([0, 5]).range([0, 1])
  const colorGradient = interpolate("#7caed7", "#303463")

  const svg = select(baseMapRef.current)
  useEffect(() => {
    svg.attr("title", "US Map")

    const paths = svg.append("g").attr("id", "paths").attr("data-testid", "basemapsvg")

    /* SVG Body -- the visible map features are described here */
    paths
      .selectAll("path")
      .data(geoData.features)
      .enter()
      .append("path")
      .classed("state", true)
      .attr("title", (d) => d.properties.name)
      .attr("d", path)
      .attr("fill", (d: Feature) => "lightblue")
      .attr("stroke", "white")
      .attr("cursor", "pointer")
      .attr("pointer-events", "all")

    return () => {
      paths.remove()
    }
  }, [valueScale, path, colorGradient, geoData, svg])

  return (
    <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}>
    </svg>
  )
}
