import * as React from "react"
import { Link, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import DetailCard from "./DetailCard"
import UnitListItem from "@/components/unit/UnitListItem"

interface MostReportedUnitsProps {
  most_reported_units?: SearchResponse[]
  total_units?: number
}

export default function MostReportedUnits({
  most_reported_units,
  total_units
}: MostReportedUnitsProps) {
  const totalUnits = total_units || 0

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
          Most Reported Units
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
            {totalUnits} units established
          </Typography>
          <Link href="#" variant="body2" color="inherit">
            View all
          </Link>
        </div>
      </div>
      <DetailCard>
        {most_reported_units && most_reported_units.length > 0 ? (
          most_reported_units.map((unit, index) => (
            <UnitListItem
              key={unit.uid}
              unit={unit}
              outlined={false}
              isFirst={index === 0}
              isLast={index === most_reported_units.length - 1}
            />
          ))
        ) : (
          <div>No units reported.</div>
        )}
      </DetailCard>
    </>
  )
}
