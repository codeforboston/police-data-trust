//@ts-nocheck
import * as d3 from "d3"
import { useEffect, useRef, useState } from "react"

export function MarkerLayer({ data, projection }) {
  const ref = useRef()
  const svg = d3.select(ref.current)

  const [circles, setCircles] = useState([])
  const path = d3.geoPath()
  const circleGenerator = d3.geoCircle()

  useEffect(() => {
    if (!data) return

    const populationScale = d3
      .scaleLinear()
      .domain(d3.extent(data.data.features, (d) => d.properties.population))
      .range([1, 50])

    const dataCircs = data.data.features.slice(0, 100).map((d, i) => {
      const circ = circleGenerator({
        r: populationScale(d.properties.population),
        center: d.geometry.coordinates,
      })
      return {
        center: projection(d.geometry.coordinates),
        path: path(circ),
        population: populationScale(d.properties.population),
      }
    })

    setCircles(dataCircs)
  }, [data])

  return (
    <svg ref={ref} viewBox="0, 0, 1200, 700" className="marker-layer">
      {circles.map((c, i) => (
        <circle
          className="circle-marker"
          cx={c.center[0]}
          cy={c.center[1]}
          r={c.population}
          key={`${i}${c.population}`}
          fill="transparent"
          stroke="green"
          strokeWdth="3"
        />
      ))}
    </svg>
  )
}
