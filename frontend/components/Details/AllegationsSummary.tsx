import * as React from "react"
import { Link, Typography } from "@mui/material"
import { AllegationSummary } from "@/utils/api"
import DetailCard from "./DetailCard"

interface AllegationsSummaryProps {
  allegation_summary?: AllegationSummary[]
}

export default function AllegationsSummary({ allegation_summary }: AllegationsSummaryProps) {
  const totalComplaints = allegation_summary?.reduce((sum, a) => sum + a.complaint_count, 0) || 0
  const totalAllegations = allegation_summary?.reduce((sum, a) => sum + a.count, 0) || 0
  const totalSubstantiated =
    allegation_summary?.reduce((sum, a) => sum + a.substantiated_count, 0) || 0

  return (
    <>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "16px",
          marginTop: "32px",
          marginBottom: "16px"
        }}
      >
        <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
          Allegations
        </Typography>
        {allegation_summary && allegation_summary.length > 0 && (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexGrow: 1
            }}
          >
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              {totalComplaints} complaints · {totalAllegations} allegations · {totalSubstantiated}{" "}
              substantiated
            </Typography>
            <Link href="#" variant="body2" color="inherit">
              View all
            </Link>
          </div>
        )}
      </div>
      <DetailCard>
        {allegation_summary && allegation_summary.length > 0 ? (
          allegation_summary.map((allegation, index) => (
            <div
              key={index}
              style={{
                padding: "20px 28px"
              }}
            >
              <div style={{ fontWeight: "600", fontSize: "1rem", marginBottom: "8px" }}>
                {allegation.type}
              </div>
              <div style={{ fontSize: "0.9rem", fontWeight: 500, color: "#303030" }}>
                <div>
                  {allegation.complaint_count} complaints, {allegation.count} allegations,{" "}
                  {allegation.substantiated_count} substantiated,{" "}
                  {allegation.earliest_incident_date || allegation.latest_incident_date ? (
                    <>
                      {allegation.earliest_incident_date
                        ? new Date(allegation.earliest_incident_date).getFullYear()
                        : "Unknown"}{" "}
                      -{" "}
                      {allegation.latest_incident_date
                        ? new Date(allegation.latest_incident_date).getFullYear()
                        : "Unknown"}
                    </>
                  ) : null}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div>No allegations available.</div>
        )}
      </DetailCard>
    </>
  )
}
