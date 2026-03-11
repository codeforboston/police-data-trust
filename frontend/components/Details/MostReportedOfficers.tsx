import * as React from "react"
import { Link, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import DetailCard from "./DetailCard"
import OfficerListItem from "@/components/officer/OfficerListItem"

interface MostReportedOfficersProps {
  reported_officers?: SearchResponse[]
  total_officers?: number
}

export default function MostReportedOfficers({ reported_officers, total_officers }: MostReportedOfficersProps) {
  const totalOfficers = total_officers || 0

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
          Most Reported Officers
        </Typography>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexGrow: 1
            }}
          >
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              {totalOfficers} known officers
            </Typography>
            <Link href="#" variant="body2" color="inherit">
              View all
            </Link>
          </div>
      </div>
      <DetailCard>
        {reported_officers && reported_officers.length > 0 ? (
          reported_officers.map((officer, index) => (
            <OfficerListItem
              key={officer.uid}
              officer={officer}
              outlined={false}
              isFirst={index === 0}
              isLast={index === reported_officers.length - 1}
            />
          ))
        ) : (
          <div>No officers reported.</div>
        )}
      </DetailCard>
    </>
  )
}
