import { geoPath, scaleLinear, interpolate, select } from "d3"
import { Feature, FeatureCollection } from "geojson"
import React, { useEffect, useRef, useState } from "react"

// colors:
// --darkBlue: #303463;
// --lightBlue: #7caed7;
// --grey: #666666;
// --red: #bf1212;
// --linkBlue: #0645ad;
// --white: #ffffff;

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
    // if (!geoData) return
    // Set the title after loading data to facilitate testing
    svg.attr("title", "US Map")

    /* Definitions -- this section defines the special styling which 
    will be applied to the features of the map */

    // const defs = svg.append("defs")

    // const strokeShape = defs.append("filter").attr("id", "strokeShape")

    // strokeShape
    //   .append("feMorphology")
    //   .attr("operator", "erode")
    //   .attr("radius", 1)
    //   .attr("result", "erode")

    // strokeShape
    //   .append("feGaussianBlur")
    //   .attr("in", "erode")
    //   .attr("stdDeviation", "3")
    //   .attr("result", "blurFilter")

    // strokeShape
    //   .append("feColorMatrix")
    //   .attr("id", "colorMatrix2")
    //   .attr("in", "blurFilter")
    //   .attr("mode", "matrix")
    //   .attr("values", "1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 14 -7")
    //   .attr("result", "colorMatrix2")

    // strokeShape
    //   .append("feGaussianBlur")
    //   .attr("in", "erode")
    //   .attr("stdDeviation", "2")
    //   .attr("result", "blurFilter2")

    // strokeShape
    //   .append("feComposite")
    //   .attr("in", "colorMatrix2")
    //   .attr("in2", "blurFilter2")
    //   .attr("operator", "out")
    //   .attr("result", "compositedStroke")

    // strokeShape
    //   .append("feBlend")
    //   .attr("in", "colorMatrix2")
    //   .attr("in2", "compositedStroke")
    //   .attr("mode", "multiply")

    const paths = svg.append("g").attr("id", "paths")

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
      // defs.remove()
      paths.remove()
    }
  }, [valueScale, path, colorGradient, geoData, svg])

  return (
    <svg id="map" viewBox={`0, 0, 1200, 700`} ref={baseMapRef}>
      <rect
        height={100}
        width={100}
        x={100}
        y={100}
        fill={"yellow"}
        onClick={() => {
          console.log(reload)
          setReload(reload + 1)
        }}
      />
    </svg>
  )
}
