import * as d3 from "d3"
import { useEffect, useRef } from "react"
import styles from "./bubble-chart.module.css"

interface BubbleData {
  officerName: string
  location: string
  incidents: number
}

interface BubbleNode extends BubbleData {
  children?: BubbleNode[]
}

const bubbleTree: BubbleNode = {
  officerName: "Root",
  location: "",
  incidents: 0,
  children: [
    {
      officerName: "Sgt. Jason Smith",
      location: "New York PD",
      incidents: 846
    },
    {
      officerName: "Lt. Jason Smith",
      location: "Seattle PD",
      incidents: 92
    },
    {
      officerName: "Sgt. Jason Smith",
      location: "Hoover Sherriff",
      incidents: 8
    },
    {
      officerName: "Cpt. Jason Smith",
      location: "Tampa PD",
      incidents: 742
    },
    {
      officerName: "Dep. Jason Smith",
      location: "Honolulu PD",
      incidents: 12
    },
    {
      officerName: "Cpt. Sarah Johnson",
      location: "Chicago PD",
      incidents: 950
    },
    {
      officerName: "Sgt. Emily Davis",
      location: "Los Angeles PD",
      incidents: 347
    },
    {
      officerName: "Lt. Michael Brown",
      location: "Dallas PD",
      incidents: 580
    },
    {
      officerName: "Dep. Amanda White",
      location: "Miami PD",
      incidents: 49
    },
    {
      officerName: "Cpt. Robert Miller",
      location: "Phoenix PD",
      incidents: 15
    }
  ]
}

const renderBubbleText = (
  data: BubbleNode,
  r: number,
  colorScale: d3.ScaleOrdinal<string, string, never>
) => {
  const dummy = document.createElement("div")
  const circleColor = colorScale(data.officerName)
  const fillColor = circleColor === "#303463" ? "white" : "black"

  const bubbleText = document.createElement("div")
  bubbleText.style.display = "flex"
  bubbleText.style.flexDirection = "column"
  bubbleText.style.justifyContent = "center"
  bubbleText.style.alignItems = "center"
  bubbleText.style.height = "100%"
  bubbleText.style.color = fillColor

  // Officer Name Element
  const officerName = document.createElement("tspan")
  officerName.textContent = data.officerName
  officerName.style.fontWeight = "bold"
  officerName.style.textAlign = "center"

  // Location Element
  const location = document.createElement("tspan")
  location.textContent = data.location

  // Incident Element
  const incidents = document.createElement("tspan")
  incidents.textContent = `${data.incidents} Incidents`

  bubbleText.append(officerName)
  bubbleText.append(location)
  bubbleText.append(incidents)

  dummy.append(bubbleText)

  return r > 40 ? dummy.innerHTML : ""
}

export default function BubbleChart() {
  const svgRef = useRef<SVGSVGElement>(null)

  const updateSVG = () => {
    const svg = d3.select(svgRef.current)

    const root = d3.hierarchy<BubbleNode>(bubbleTree)
    const pack = d3.pack<BubbleNode>().size([300, 300]).padding(5)

    root.sum((d) => d.incidents || 0).sort((a, b) => b.data.incidents - a.data.incidents)
    const packedHierarchy = pack(root)

    const colorScale = d3
      .scaleOrdinal<string>()
      .domain(packedHierarchy.leaves().map((d) => d.data.officerName))
      .range(["#BBDDF8", "#7CAED7", "#303463"])

    svg.selectAll("*").remove()

    // Add drop shadow to SVG
    svg
      .append("defs")
      .append("filter")
      .attr("id", "drop-shadow")
      .attr("width", "150%")
      .attr("height", "150%")
      .append("feDropShadow")
      .attr("dx", 0)
      .attr("dy", 2)
      .attr("stdDeviation", 1)
      .attr("flood-color", "rgba(0,0,0,0.5)")

    // Add bubbles to SVG
    svg
      .selectAll("circle")
      .data(packedHierarchy.leaves())
      .enter()
      .append("circle")
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y)
      .attr("r", (d) => d.r)
      .attr("fill", (d) => colorScale(d.data.officerName))
      .attr("opacity", 0.7)
      .style("filter", "url(#drop-shadow)")

    // Add bubble text to SVG
    svg
      .selectAll("foreignObject")
      .data(packedHierarchy.leaves())
      .enter()
      .append("foreignObject")
      .attr("width", (d) => d.r * 2)
      .attr("height", (d) => d.r * 2)
      .html(({ data, r }) => renderBubbleText(data, r, colorScale))
      .attr("x", (d) => d.x - d.r)
      .attr("y", (d) => d.y - d.r)
      .attr("font-size", "11px")

    // Adjust viewBox to fit the entire graphic
    const minX = d3.min(packedHierarchy.leaves(), (d) => d.x - d.r)
    const minY = d3.min(packedHierarchy.leaves(), (d) => d.y - d.r)
    const width = d3.max(packedHierarchy.leaves(), (d) => d.x + d.r - minX)
    const height = d3.max(packedHierarchy.leaves(), (d) => d.y + d.r - minY)

    svg.attr("viewBox", `${minX - 5} ${minY - 5} ${width + 10} ${height + 10}`)
  }

  useEffect(() => {
    updateSVG()
  }, [])

  return (
    <object className={styles.svgContainer}>
      <svg ref={svgRef} className={styles.svg} />
    </object>
  )
}
