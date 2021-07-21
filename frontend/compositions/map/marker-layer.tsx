//@ts-nocheck
import * as d3 from "d3"
import { Polygon } from "geojson"
import { useEffect, useState } from "react"

type MarkerLayerProps = {
  data: {},
  projection: d3.GeoProjection,
}

type Coord = [number, number]

type CircleDescription = {
  center: Coord
  path: string
  population: number,
  city: string
}

export function MarkerLayer(props: MarkerLayerProps) {
  const [circles, setCircles] = useState<Polygon>([])
  const path = d3.geoPath()
  const circleGenerator = d3.geoCircle()
  const { data, projection} = props

  useEffect(() => {
    if (!data) return

    const populationScale = d3
      .scaleLinear()
      .domain(d3.extent(data.data.features, (d) => d.properties.population))
      .range([1, 50])

    
    const dataCircs: CircleDescription[] = data.data.features.slice(0, 100).map((d) => {
    
      // population data, coordinates from dummy data set
      const {
        properties: { population, city },
        geometry: { coordinates },
      } = d

      const circ = circleGenerator({
        r: populationScale(population),
        center: coordinates,
      })

      return {
        center: projection(coordinates),
        path: path(circ),
        population: populationScale(population),
        city: city
      }
    })

    setCircles(dataCircs)
  }, [data])

  return (
    <svg viewBox="0, 0, 1200, 700" className="marker-layer" height={"100%"} width={"100%"} >
      {circles.map((c, i) => (
        <circle
          className="circle-marker"
          cx={c.center[0]}
          cy={c.center[1]}
          r={c.population}
          key={`${i}${c.population}`}
          fill="#2572"
          stroke="green"
          strokeWidth="3"
          onClick={() => console.log(c.city)}
        />
      ))}
    </svg>
  )
}
