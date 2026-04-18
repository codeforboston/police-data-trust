"use client"

import React from "react"
import { Card, CardContent, Typography } from "@mui/material"
import { SourceActivity } from "@/utils/api"

const CHART_WIDTH = 500
const CHART_HEIGHT = 260
const PADDING_X = 42
const PADDING_Y = 18

const PIE_COLORS = ["#D500F9", "#2196F3", "#26A69A", "#FB8C00", "#8E24AA", "#546E7A"]

const formatDateLabel = (date: string) =>
  new Date(`${date}T00:00:00`).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric"
  })

const formatLastActive = (timestamp: string | null) => {
  if (!timestamp) return "No recorded activity yet"

  return `Last active ${new Date(timestamp).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  })}`
}

function LineChart({ data }: { data: SourceActivity["contributions_over_time"] }) {
  if (!data.length) {
    return <Typography color="text.secondary">No contributions recorded yet.</Typography>
  }

  const maxValue = Math.max(...data.map((point) => point.count), 1)
  const chartInnerWidth = CHART_WIDTH - PADDING_X * 2
  const chartInnerHeight = CHART_HEIGHT - PADDING_Y * 2

  const points = data.map((point, index) => {
    const x =
      PADDING_X + (data.length === 1 ? chartInnerWidth / 2 : (index / (data.length - 1)) * chartInnerWidth)
    const y =
      PADDING_Y + chartInnerHeight - (point.count / maxValue) * chartInnerHeight

    return { ...point, x, y }
  })

  const path = points.map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ")
  const ticks = Array.from({ length: 5 }, (_, index) => Math.round((maxValue * (4 - index)) / 4))

  return (
    <svg width="100%" viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`} role="img" aria-label="Contribution history">
      {ticks.map((tick) => {
        const y = PADDING_Y + chartInnerHeight - (tick / maxValue) * chartInnerHeight
        return (
          <g key={tick}>
            <line
              x1={PADDING_X}
              x2={CHART_WIDTH - PADDING_X}
              y1={y}
              y2={y}
              stroke="#E0E0E0"
              strokeWidth="1"
            />
            <text x={PADDING_X - 10} y={y + 4} textAnchor="end" fontSize="12" fill="#444">
              {tick}
            </text>
          </g>
        )
      })}

      <line
        x1={PADDING_X}
        x2={PADDING_X}
        y1={PADDING_Y}
        y2={CHART_HEIGHT - PADDING_Y}
        stroke="#222"
        strokeWidth="1"
      />
      <line
        x1={PADDING_X}
        x2={CHART_WIDTH - PADDING_X}
        y1={CHART_HEIGHT - PADDING_Y}
        y2={CHART_HEIGHT - PADDING_Y}
        stroke="#222"
        strokeWidth="1"
      />

      <path d={path} fill="none" stroke="#D500F9" strokeWidth="3" strokeLinejoin="round" />

      {points.map((point) => (
        <g key={point.date}>
          <circle cx={point.x} cy={point.y} r="5" fill="#fff" stroke="#D500F9" strokeWidth="2" />
          <text x={point.x} y={CHART_HEIGHT - 8} textAnchor="middle" fontSize="12" fill="#444">
            {formatDateLabel(point.date)}
          </text>
        </g>
      ))}
    </svg>
  )
}

function polarToCartesian(cx: number, cy: number, r: number, angle: number) {
  const radians = ((angle - 90) * Math.PI) / 180
  return {
    x: cx + r * Math.cos(radians),
    y: cy + r * Math.sin(radians)
  }
}

function PieChart({ data }: { data: SourceActivity["contribution_locations"] }) {
  if (!data.length) {
    return <Typography color="text.secondary">No location data available yet.</Typography>
  }

  const total = data.reduce((sum, slice) => sum + slice.count, 0)
  const radius = 88
  const center = 110
  let startAngle = 0

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "24px", flexWrap: "wrap", justifyContent: "center" }}>
      <svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="Contribution locations">
        {data.map((slice, index) => {
          const sweep = (slice.count / total) * 360
          const endAngle = startAngle + sweep
          const largeArcFlag = sweep > 180 ? 1 : 0
          const start = polarToCartesian(center, center, radius, startAngle)
          const end = polarToCartesian(center, center, radius, endAngle)
          const path = [
            `M ${center} ${center}`,
            `L ${start.x} ${start.y}`,
            `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${end.x} ${end.y}`,
            "Z"
          ].join(" ")
          const fill = PIE_COLORS[index % PIE_COLORS.length]
          startAngle = endAngle

          return <path key={slice.label} d={path} fill={fill} stroke="#fff" strokeWidth="2" />
        })}
      </svg>

      <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        {data.map((slice, index) => (
          <div key={slice.label} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <span
              style={{
                width: "18px",
                height: "18px",
                borderRadius: "4px",
                backgroundColor: PIE_COLORS[index % PIE_COLORS.length],
                flexShrink: 0
              }}
            />
            <Typography sx={{ fontSize: "16px", lineHeight: "20px" }}>
              {slice.label} ({slice.count})
            </Typography>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function ActivityCard({ activity }: { activity: SourceActivity | null }) {
  return (
    <Card
      variant="outlined"
      sx={{
        marginTop: "20px",
        marginBottom: "20px",
        borderColor: "#CCCCCC",
        borderRadius: "10px"
      }}
    >
      <CardContent
        sx={{
          p: "48px",
          "&:last-child": { pb: "48px" },
          "@media (max-width:430px)": {
            p: "24px",
            "&:last-child": { pb: "24px" }
          },
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "32px"
        }}
      >
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px" }}>
          <Typography
            variant="h5"
            fontWeight={600}
            sx={{ fontFamily: "Inter, Roboto, sans-serif", fontSize: "24px", lineHeight: "29px" }}
          >
            Activity
          </Typography>
          <Typography variant="body1" sx={{ color: "#757575", fontSize: "16px", lineHeight: "19px" }}>
            {formatLastActive(activity?.last_active_at || null)}
          </Typography>
        </div>

        <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: "40px", alignItems: "center" }}>
          <div style={{ width: "100%", maxWidth: "500px", display: "flex", flexDirection: "column", alignItems: "center", gap: "12px" }}>
            <Typography sx={{ fontSize: "16px", lineHeight: "19px" }}>Contribution History</Typography>
            <LineChart data={activity?.contributions_over_time || []} />
          </div>

          <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center", gap: "12px" }}>
            <Typography sx={{ fontSize: "16px", lineHeight: "19px" }}>Locations of Contributions</Typography>
            <PieChart data={activity?.contribution_locations || []} />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
