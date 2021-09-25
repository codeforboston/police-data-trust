import { select } from "d3"
import { useEffect } from "react"
import { DataPoint, JoinSelection } from "../utilities/chartTypes"

export function Bubbles(props: { data: DataPoint[] }) {
  const { data } = props
  useEffect(() => {
    if (!data) return
    const container = select("#chart-root g")
    console.log(data)
    container.selectAll("g").data(data).join(joinEnter, joinUpdate, joinExit)
  }, [data])

  return (
    <svg id="chart-root" viewBox="0 0 1200 700" width="80vw">
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
    .html((d) => d.label + "<br>" + d.value)
    .call(setTextAttrs)
  return selection
}

function setGroupAttrs(selection: JoinSelection) {
  return selection.attr("transform", (d: DataPoint) => `translate(${d.coord.x}, ${d.coord.y})`)
}

function setCircleAttrs(selection: JoinSelection) {
  return selection
    .transition()
    .duration(1000)
    .attr("r", (d) => d.r || 1)
    .attr("fill", (d) => d.fill)
}

function setForeignObjectAttrs(selection: JoinSelection) {
  return selection
    .attr("height", (d) => (d.r ? d.r * 2 : 2))
    .attr("width", (d) => (d.r ? d.r * 2 : 2))
    .attr("x", (d) => (d.r ? -d.r : 0))
    .attr("y", (d) => (d.r ? -d.r : 0))
}

function setTextAttrs(selection: JoinSelection) {
  selection
    .style("text-align", "center")
    .style("color", "white")
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
    .attr("r", (d) => (d.r ? d.r : 1))
    .attr("fill", (d) => d.fill)
    .selection()
}

function transitionGroupAttrs(selection: JoinSelection) {
  return selection
    .transition()
    .duration(1000)
    .attr("transform", (d: DataPoint) => `translate(${d.coord.x}, ${d.coord.y})`)
}
