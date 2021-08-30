import * as d3 from "d3"
import { extent, HierarchyCircularNode, max, min, scaleLinear } from "d3"
import { Feature } from "geojson"
import React, { useCallback, useEffect, useState } from "react"
import useData, { CityProperties, Data } from "../map/useData"
import { Coord, Pair, DataPoint, PackableObj } from "./chartTypes"
import styles from "./bubble.module.css"
import { lightBlueGrey, lightDarkBlueTheme } from "./chartScales"

//d3 force, d3 hierarchy

export function createColorScale(minMax: Pair<number>) {
  return scaleLinear().domain(minMax).range([0, 1])
}

export function Bubble(props: DataPoint) {
  const { shape, value, coord, fill, stroke, strokeWidth } = props
  if (shape !== "circle") throw "shape must be circle"
  const { x, y } = coord
  return <circle r={value} cx={x} cy={y} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />
}
export function SquareBubble(props: DataPoint) {
  const { shape, value, coord, fill, stroke, strokeWidth } = props
  if (shape !== "square") throw "shape must be square"
  const { x, y } = coord
  return (
    <rect
      height={value}
      width={value}
      x={x}
      y={y}
      fill={fill}
      stroke={stroke}
      strokeWidth={strokeWidth}
    />
  )
}

export default function BubbleChart() {
  const rawData: Data = useData()
  const [filter, setFilter] = useState({ property: "city", value: "all", limit: 50 })
  const [data, setData] = useState<CityProperties[]>([])
  const [shift, setShift] = useState(10)

  useEffect(() => {
    if (!rawData) return

    rawData.setFilterProperties(filter)

    const cityProperties = rawData.features.map((f) => getProperties(f) as CityProperties)

    setData(cityProperties)
  }, [rawData, filter])

  const symbolData = useCallback((): DataPoint[] => {
    if (!data) return []

    const root = packPop(formatPackProperties(data.slice(shift)) as PackableObj)

    const minMax = extent(root.leaves().map((l) => l.value))

    const scaleColor = createColorScale(minMax)

    const symbolPropsArray = root.leaves().map((leaf) => {
      return {
        shape: "circle",
        value: 60 * scaleColor(leaf.value),
        coord: { x: leaf.x, y: leaf.y },
        fill: lightDarkBlueTheme(scaleColor(leaf.value))
      }
    })

    return symbolPropsArray
  }, [data])

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row"}}>
        <div className={styles.background}>
          <button
            type="button"
            className="primaryButton"
            onClick={() => {
              setFilter((filter) => {
                return { ...filter, limit: filter.limit + 10 }
              })
            }}>
            More
          </button>
          <button
            type="button"
            className="primaryButton"
            onClick={() => {
              setFilter((filter) => {
                return { ...filter, limit: filter.limit - 10 }
              })
            }}>
            Less
          </button>
        </div>
        <svg id="chart-root" viewBox="0 0 1200 700" height="700" width="1200">
          {symbolData().map((props: DataPoint, i: number) => (
            <Bubble key={i} {...props} />
          ))}
        </svg>
        1
      </div>
    </>
  )
}

function packPop(data: PackableObj): HierarchyCircularNode<PackableObj> {
  return d3
    .pack()
    .size([1200 - 2, 700 - 2])
    .padding(3)(
    d3
      .hierarchy(data)
      .sum((d) => d.population)
      .sort((a, b) => b.value - a.value)
  )
}

function formatPackProperties(
  data: CityProperties | CityProperties[]
): PackableObj | CityProperties {
  return Array.isArray(data)
    ? ({
        name: "cities",
        children: data.map((d) => formatPackProperties(d))
      } as PackableObj)
    : (data as CityProperties)
}

function getProperties(feature: Feature) {
  const properties = feature.properties as CityProperties
  const numZips: number[] = (properties.zips as string).split(" ").map((i) => Number(i))
  const boolMilitary: boolean = (properties.military as string).match(/true/i) !== null
  const boolIncorporated: boolean = (properties.incorporated as string).match(/true/i) !== null
  return {
    ...properties,
    zips: numZips,
    military: boolMilitary,
    incorporated: boolIncorporated
  }
}

/*     circleGroup
      .append("g")
      .selectAll("circle")
      .data(root.leaves())
      .enter()
      .append("circle")
      .attr("r", (d) => d.r)
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y)
      .attr("fill", "var(--darkBlue)")
      .attr("opacity", (d) => popToColor(d.value))

    circleGroup
      .append("g")
      .selectAll("circle")
      .data(root.leaves())
      .enter()
      .append("circle")
      .attr("r", (d) => d.r)
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y)
      .attr("fill", "var(--lightBlue)")
      .attr("opacity", (d) => 1 - popToColor(d.value))

    circleGroup
      .append("g")
      .selectAll("g")
      .data(root.leaves())
      .enter()
      .append("g")
      .attr("transform", (d) => `translate(${d.x}, ${d.y})`)
      .append("text")
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .text((d) => d.data.city)
      .attr("transform", (d) => `scale(${popToSize(d.value)})`)
 */
/* interface Bubble {
  cx: number
  cy: number
  r: number
  text: string
  fill?: string
  onclick?: (args: any) => void
}

function Bubble(props: Bubble) {
  const { cx, cy, r, fill, text, onclick } = props

  const [nameVisible, setNameVisible] = useState<boolean>(false)

  return (
    <g>
      <circle
        className={"bubble"}
        style={{ textAlign: "center" }}
        cx={cx}
        cy={cy}
        r={r}
        fill={fill}
        onClick={onclick}
        onMouseEnter={() => setNameVisible(true)}
        onMouseLeave={() => setNameVisible(false)}></circle>
      <text
        x={cx}
        y={cy}
        style={{
          opacity: nameVisible ? 1 : 0,
          transition: "opacity 500ms linear",
          pointerEvents: "none",
          zIndex: nameVisible ? 10 : 0,
        }}>
        {text}
      </text>
    </g>
  )
}
 */

// const popToSize = d3.scaleLinear().domain([minPop, maxPop]).range([0.5, 1])
// const populationScale = d3.scaleLinear().domain([minPop, maxPop]).range([40, 70])
// const cityIDScale = d3.scaleLinear().domain([10000000, 1000000000]).range([0, 200])
// const densityScale = d3.scaleLinear().domain([1000, 5000]).range([0, 100])
// const popToColor = d3.scaleLinear().domain([minPop, maxPop]).range([0, 1])
