"use client"

import React from "react"
import { Box, Card, CardContent, CircularProgress, Typography } from "@mui/material"
import { BarChart, PieChart } from "@mui/x-charts"
import { SourceActivity } from "@/utils/api"

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

function ContributionHistoryChart({ data }: { data: SourceActivity["contributions_over_time"] }) {
  return (
    <BarChart
      height={295}
      margin={{ top: 20, right: 20, bottom: 60, left: 50 }}
      xAxis={[
        {
          scaleType: "band",
          data: data.map((point) => point.date),
          valueFormatter: formatDateLabel,
          tickLabelStyle: {
            fontSize: 12
          }
        }
      ]}
      yAxis={[
        {
          tickLabelStyle: {
            fontSize: 12
          }
        }
      ]}
      series={[
        {
          id: "contributions",
          label: "Contributions",
          data: data.map((point) => point.count),
          color: "#D500F9",
          layout: "vertical"
        }
      ]}
      grid={{ horizontal: true }}
      hideLegend
      sx={{
        width: "100%",
        "& .MuiBarElement-root": {
          rx: 6,
          ry: 6
        }
      }}
    />
  )
}

function ContributionLocationChart({ data }: { data: SourceActivity["contribution_locations"] }) {
  if (!data.length) {
    return <Typography color="text.secondary">No location data available yet.</Typography>
  }

  return (
    <PieChart
      height={260}
      margin={{ top: 10, right: 180, bottom: 10, left: 10 }}
      hideLegend={false}
      series={[
        {
          data: data.map((slice, index) => ({
            id: slice.label,
            value: slice.count,
            label: `${slice.label} (${slice.count})`,
            color: PIE_COLORS[index % PIE_COLORS.length]
          })),
          innerRadius: 0,
          outerRadius: 90,
          paddingAngle: 2,
          cornerRadius: 4
        }
      ]}
      slotProps={{
        legend: {
          direction: "vertical",
          position: {
            vertical: "middle",
            horizontal: "end"
          },
          sx: {
            "& .MuiChartsLegend-label": {
              fontSize: 16
            }
          }
        }
      }}
      sx={{
        width: "100%"
      }}
    />
  )
}

export default function ActivityCard({
  activity,
  loading = false
}: {
  activity: SourceActivity | null
  loading?: boolean
}) {
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
          <Typography
            variant="body1"
            sx={{ color: "#757575", fontSize: "16px", lineHeight: "19px" }}
          >
            {formatLastActive(activity?.last_active_at || null)}
          </Typography>
        </div>

        <div
          style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            gap: "40px",
            alignItems: "center"
          }}
        >
          <div
            style={{
              width: "100%",
              maxWidth: "500px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "12px"
            }}
          >
            <Typography sx={{ fontSize: "16px", lineHeight: "19px" }}>
              Contribution History
            </Typography>
            {loading ? (
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  minHeight: 295
                }}
              >
                <CircularProgress
                  size={24}
                  aria-label="activity loading indicator"
                  data-testid="activity-loading-spinner"
                />
              </Box>
            ) : (
              <ContributionHistoryChart data={activity?.contributions_over_time || []} />
            )}
          </div>

          <div
            style={{
              width: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "12px"
            }}
          >
            <Typography sx={{ fontSize: "16px", lineHeight: "19px" }}>
              Locations of Contributions
            </Typography>
            {loading ? (
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  minHeight: 260
                }}
              >
                <CircularProgress
                  size={24}
                  aria-label="activity loading indicator"
                  data-testid="activity-loading-spinner"
                />
              </Box>
            ) : (
              <ContributionLocationChart data={activity?.contribution_locations || []} />
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
