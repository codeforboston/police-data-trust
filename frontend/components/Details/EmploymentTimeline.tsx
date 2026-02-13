import * as React from "react"
import Timeline from "@mui/lab/Timeline"
import TimelineItem from "@mui/lab/TimelineItem"
import TimelineSeparator from "@mui/lab/TimelineSeparator"
import TimelineConnector from "@mui/lab/TimelineConnector"
import TimelineContent from "@mui/lab/TimelineContent"
import TimelineDot from "@mui/lab/TimelineDot"
import TimelineOppositeContent, {
  timelineOppositeContentClasses
} from "@mui/lab/TimelineOppositeContent"
import { Typography } from "@mui/material"
import { EmploymentHistory } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

interface EmploymentTimelineProps {
  employment_history?: EmploymentHistory[]
}

const formatMonthYear = (dateString: string | null | undefined): string => {
  if (!dateString) return "Unknown"
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { month: "short", year: "numeric" }).replace(" ", ", ")
  } catch {
    return "Unknown"
  }
}

const getStateName = (abbreviation: string | undefined): string => {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

export default function EmploymentTimeline({ employment_history }: EmploymentTimelineProps) {
  if (!employment_history || employment_history.length === 0) {
    return <div>No employment history available.</div>
  }

  const sortedEmployment = [...employment_history].sort((a, b) => {
    // Entries with no latest_date (present) go first
    if (!a.latest_date && b.latest_date) return -1
    if (a.latest_date && !b.latest_date) return 1

    // Then sort by latest_date descending (most recent first)
    const dateA = new Date(a.latest_date || a.earliest_date || 0).getTime()
    const dateB = new Date(b.latest_date || b.earliest_date || 0).getTime()
    return dateB - dateA
  })

  return (
    <Timeline
      sx={{
        [`& .${timelineOppositeContentClasses.root}`]: {
          flex: 0.25,
          paddingLeft: 0,
          paddingRight: 2,
          minWidth: 140
        }
      }}
    >
      {sortedEmployment.map((employment, index) => (
        <TimelineItem key={index}>
          <TimelineOppositeContent sx={{ m: "0" }} align="right" variant="body2">
            {employment.earliest_date || employment.latest_date ? (
              <span>
                {formatMonthYear(employment.earliest_date)} –{" "}
                {employment.latest_date ? formatMonthYear(employment.latest_date) : "Present"}
              </span>
            ) : (
              <span>Unknown Period</span>
            )}
          </TimelineOppositeContent>

          <TimelineSeparator>
            <TimelineDot variant="filled" />
            {index < sortedEmployment.length - 1 && <TimelineConnector />}
          </TimelineSeparator>

          <TimelineContent>
            <Typography component="span" sx={{ fontWeight: "500", fontSize: "14px" }}>
              {employment.highest_rank || "Officer"}
              {employment.unit_name &&
                employment.unit_name != "Unknown" &&
                `, ${employment.unit_name}`}
            </Typography>
            <Typography variant="body2" sx={{ color: "#1E1E1E" }}>
              {employment.agency_name}
              {employment.state && `, ${getStateName(employment.state)}`}
            </Typography>
          </TimelineContent>
        </TimelineItem>
      ))}
    </Timeline>
  )
}
