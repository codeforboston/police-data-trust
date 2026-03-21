import React, { useState } from "react"
import { Typography } from "@mui/material"
import { EmploymentHistory } from "@/utils/api"
import EmploymentTimeline from "./EmploymentTimeline"
import DetailCard from "./DetailCard"

interface EmploymentProps {
  employment_history?: EmploymentHistory[]
}

export default function Employment({ employment_history }: EmploymentProps) {
  const timelineRef = React.useRef<HTMLDivElement>(null)
  const [showScroll, setShowScroll] = useState(false)

  React.useEffect(() => {
    if (timelineRef.current) {
      setShowScroll(timelineRef.current.scrollHeight > 196)
    }
  }, [employment_history])
  return (
    <>
      <Typography variant="body1" sx={{ marginTop: "32px", marginBottom: "16px" }}>
        Employment records
      </Typography>
      <DetailCard>
        <div style={{ position: "relative" }}>
          <div
            ref={timelineRef}
            style={{
              maxHeight: showScroll ? 196 : "auto",
              overflowY: showScroll ? "auto" : "visible"
            }}
          >
            <EmploymentTimeline employment_history={employment_history} />
            {showScroll && (
              <Typography
                color="text.secondary"
                sx={{
                  display: "flex",
                  width: "100%",
                  justifyContent: "center",
                  backgroundColor: "white",
                  fontSize: "14px",
                  fontWeight: "500",
                  position: "absolute",
                  bottom: 0,
                  right: "50%",
                  transform: "translateX(50%)"
                }}
              >
                Scroll to see more
              </Typography>
            )}
          </div>
        </div>
      </DetailCard>
    </>
  )
}
