import * as d3 from "d3"
import { drop } from "lodash"
import React, { useEffect, useState } from "react"
import useData, { CityProperties, Data } from "../map/useData"
import styles from "./bubble.module.css"
import { funcTransition, testTransition } from "./chartD3Functions"
import { formatSymbolData, parseProperties } from "./chartDataHandlers"
import { ChartSymbolProps, DataPoint, JoinSelection, JoinTransition } from "./chartTypes"

//d3 force, d3 hierarchy

export default function BubbleChart() {
  const rawData: Data = useData()
  const [filter, setFilter] = useState({ property: "city", value: "all", lowCut: 50, limit: 80 })
  const [data, setData] = useState<CityProperties[]>([])
  const [shift, setShift] = useState(10)
  const [symbolProps, setSymbolProps] = useState<DataPoint[]>()
  const [limit, setLimit] = useState(20)
  const [lowCut, setLowCut] = useState(0)

  useEffect(() => {
    if (!rawData) return
    rawData.setFilterProperties(filter)
    const cityProperties = rawData.features.map((f) => parseProperties(f) as CityProperties)
    setData(cityProperties)
    setSymbolProps(formatSymbolData(data, shift).sort((a, b) => (a.value - b.value ? 0 : 1)))
  }, [rawData, filter])

  return (
    <>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <div className={styles.background}>
          <input
            type={"text"}
            value={lowCut}
            placeholder={filter.lowCut.toString()}
            id="lowCut"
            onChange={(event) => setLowCut(Number(event.target.value))}
          />
          <input
            type={"text"}
            value={limit}
            placeholder={filter.limit.toString()}
            id="limit"
            onChange={(event) => setLimit(Number(event.target.value))}
          />
          <button
            type="button"
            className="primaryButton"
            onClick={() => {
              setFilter((filter) => {
                return {
                  ...filter,
                  lowCut: lowCut,
                  limit: limit
                }
              })
            }}>
            Set Filter
          </button>
        </div>
        <Bubbles data={symbolProps} />
      </div>
    </>
  )
}

export function Bubbles(props: { data: DataPoint[] }) {
  const { data } = props
  useEffect(() => {
    if (!data) return
    const container = d3.select("#chart-root g")

    container.selectAll("g").data(data).join(joinEnter, joinUpdate, joinExit)
  }, [data])

  return (
    <svg id="chart-root" viewBox="0 0 1200 700" height="700" width="1200">
      <g></g>
    </svg>
  )
}

function joinEnter(enter: JoinSelection) {
  return enter.append("g").call(addCircleGroup)
}

function joinUpdate(update: JoinSelection) {
  return update.call(transitionGroupAttrs).select("circle").call(transitionCircleAttrs)
}

function joinExit(exit: JoinSelection) {
  return exit.remove()
}

function addCircleGroup(selection: JoinSelection) {
  selection.call(setGroupAttrs)
  selection.append("circle").call(setCircleAttrs)
  selection
    .append("foreignObject")
    .call(setForeignObjectAttrs)
    .append("xhtml:div")
    .html((d) => d.label)
    .call(setTextAttrs)
  return selection
}

function setGroupAttrs(selection: JoinSelection) {
  return selection.attr("transform", (d: DataPoint) => `translate(${d.coord.x}, ${d.coord.y})`)
}

function setCircleAttrs(selection: JoinSelection) {
  selection
    .transition()
    .duration(1000)
    .attr("r", (d) => d.r)
    .attr("fill", (d) => d.fill)
  return selection
}

function setForeignObjectAttrs(selection: JoinSelection) {
  return selection
    .attr("height", (d) => d.r * 2)
    .attr("width", (d) => d.r * 2)
    .attr("x", (d) => -d.r)
    .attr("y", (d) => -d.r)
}

function setTextAttrs(selection: JoinSelection) {
  selection
    .style("text-align", "center")
    .style("transform", (d) => `translate(0, ${d.r}px) translate(0, -50%)`)
    .style("opacity", 0)
    .transition()
    .duration(800)
    .delay(200)
    .style("opacity", 1)
}

function transitionCircleAttrs(selection: JoinSelection) {
  return selection
    .transition()
    .duration(1000)
    .attr("r", (d) => d.r)
    .attr("fill", (d) => d.fill)
    .selection()
}

function transitionGroupAttrs(selection: JoinSelection) {
  return selection
    .transition()
    .duration(1000)
    .attr("transform", (d: DataPoint) => `translate(${d.coord.x}, ${d.coord.y})`)
}

export function Bubble(props: DataPoint) {
  const { shape, r, coord, fill, stroke, strokeWidth } = props
  if (shape !== "circle") throw "shape must be circle"
  const { x, y } = coord
  return <circle r={r} cx={x} cy={y} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />
}
