"use client"

import { useEffect, useMemo, useState } from "react"
import { LineChart } from "@mui/x-charts/LineChart"
import Slider from "@mui/material/Slider"
import ToggleButton from "@mui/material/ToggleButton"
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import { apiFetch } from "@/utils/apiFetch"
import { useAuth } from "@/providers/AuthProvider"
import { apiBaseUrl } from "@/utils/apiRoutes"
import API_ROUTES from "@/utils/apiRoutes"
import { ComplaintsOverTimePoint } from "@/utils/api"

const WINDOW_OPTIONS = [5, 10, 20] as const
type WindowSize = (typeof WINDOW_OPTIONS)[number] | "all"
const MIN_YEAR = 1990
const MIN_VISIBLE_POINTS = 2

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max)
}

export default function OverviewPage() {
  const { accessToken, hasHydrated } = useAuth()
  const [data, setData] = useState<ComplaintsOverTimePoint[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [windowSize, setWindowSize] = useState<WindowSize>("all")
  const [range, setRange] = useState<[number, number]>([0, 0])
  const loginRequired = hasHydrated && !accessToken
  useEffect(() => {
    if (loginRequired) {
      window.dispatchEvent(new Event("npdc:login-required-search"))
    }
  }, [loginRequired])

  useEffect(() => {
    if (!hasHydrated || !accessToken) return
    let active = true

    const loadData = async (): Promise<void> => {
      try {
        const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.complaints.metricsOverTime}`)
        if (!res.ok) {
          throw new Error(`Request failed with status ${res.status}`)
        }
        const json: ComplaintsOverTimePoint[] = await res.json()
        const points = json.filter((point) => Number(point.year) >= MIN_YEAR)
        if (active) {
          setData(points)
          setRange([0, Math.max(0, points.length - 1)])
        }
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : "Failed to load data")
        }
      }
    }

    loadData()
    return () => {
      active = false
    }
  }, [hasHydrated, accessToken])

  const pointCount = data?.length ?? 0
  const lastIndex = Math.max(0, pointCount - 1)
  const selectedWindow: WindowSize =
    windowSize !== "all" && windowSize < pointCount ? windowSize : "all"
  const isAll = selectedWindow === "all"
  const presetWidth = isAll ? pointCount : selectedWindow
  const maxStartIndex = Math.max(0, pointCount - presetWidth)
  const startIndex = clamp(range[0], 0, isAll ? lastIndex : maxStartIndex)
  const endIndex = isAll
    ? clamp(range[1], startIndex, lastIndex)
    : Math.min(startIndex + presetWidth - 1, lastIndex)

  const visibleData = useMemo(
    () => (data ?? []).slice(startIndex, endIndex + 1),
    [data, startIndex, endIndex]
  )

  const handleWindowSizeChange = (_event: unknown, next: WindowSize | null): void => {
    if (next === null) return
    if (next === "all") {
      setRange([0, lastIndex])
      setWindowSize(next)
      return
    }

    const width = Math.min(next, pointCount)
    const nextStart = clamp(endIndex - width + 1, 0, Math.max(0, pointCount - width))
    setRange([nextStart, nextStart + width - 1])
    setWindowSize(next)
  }

  const handleWindowSlide = (_event: unknown, value: number | number[]): void => {
    const nextStart = value as number
    setRange([nextStart, nextStart + presetWidth - 1])
  }

  const handleRangeChange = (_event: unknown, value: number | number[], thumb: number): void => {
    const [nextStart, nextEnd] = value as [number, number]
    if (nextEnd - nextStart >= MIN_VISIBLE_POINTS - 1) {
      setRange([nextStart, nextEnd])
    } else if (thumb === 0) {
      const start = Math.min(nextStart, lastIndex - (MIN_VISIBLE_POINTS - 1))
      setRange([start, start + MIN_VISIBLE_POINTS - 1])
    } else {
      const end = Math.max(nextEnd, MIN_VISIBLE_POINTS - 1)
      setRange([end - (MIN_VISIBLE_POINTS - 1), end])
    }
  }

  if (!hasHydrated) {
    return <div style={{ padding: "1rem" }}>Loading…</div>
  }

  if (loginRequired) {
    return (
      <div role="alert" style={{ color: "red", padding: "1rem" }}>
        Please log in before searching.
      </div>
    )
  }

  if (error) {
    return <div style={{ color: "red", padding: "1rem" }}>Error: {error}</div>
  }

  if (data === null) {
    return <div style={{ padding: "1rem" }}>Loading…</div>
  }

  if (pointCount === 0) {
    return <div style={{ padding: "1rem" }}>No complaint data available.</div>
  }

  const firstVisibleYear = visibleData[0]?.year
  const lastVisibleYear = visibleData[visibleData.length - 1]?.year

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Complaints Over Time</h1>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "1rem",
          flexWrap: "wrap"
        }}
      >
        <ToggleButtonGroup
          exclusive
          size="small"
          value={selectedWindow}
          onChange={handleWindowSizeChange}
          aria-label="Number of years shown"
        >
          {WINDOW_OPTIONS.filter((option) => option < pointCount).map((option) => (
            <ToggleButton key={option} value={option}>
              {option} yrs
            </ToggleButton>
          ))}
          <ToggleButton value="all">All</ToggleButton>
        </ToggleButtonGroup>

        <span role="status" aria-live="polite">
          {firstVisibleYear === lastVisibleYear
            ? firstVisibleYear
            : `${firstVisibleYear}–${lastVisibleYear}`}
        </span>
      </div>

      <LineChart
        xAxis={[
          {
            data: visibleData.map((point) => point.year),
            scaleType: "point",
            label: "Year"
          }
        ]}
        series={[
          {
            data: visibleData.map((point) => point.complaint_count),
            label: "Complaints"
          }
        ]}
        height={400}
      />

      <div style={{ padding: "0 2rem" }}>
        {isAll ? (
          <Slider
            value={[startIndex, endIndex]}
            onChange={handleRangeChange}
            min={0}
            max={lastIndex}
            step={1}
            disableSwap
            disabled={pointCount <= MIN_VISIBLE_POINTS}
            marks
            getAriaLabel={(index) => (index === 0 ? "First year shown" : "Last year shown")}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => data[value].year}
          />
        ) : (
          <Slider
            value={startIndex}
            onChange={handleWindowSlide}
            min={0}
            max={maxStartIndex}
            step={1}
            disabled={maxStartIndex === 0}
            marks
            aria-label="Scroll through years"
            valueLabelDisplay="auto"
            valueLabelFormat={(value) =>
              `${data[value].year}–${data[Math.min(value + presetWidth - 1, lastIndex)].year}`
            }
          />
        )}
      </div>
    </div>
  )
}
