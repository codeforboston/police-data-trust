"use client"

import { Typography } from "@mui/material"
import { Unit } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedOfficers from "@/components/Details/MostReportedOfficers"
import Attachments from "../Attachments"

export default function UnitDetailsTabs(unit: Unit) {
  const tabs = [
    {
      label: "Overview",
      content: (
        <>
          <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
            Leadership
          </Typography>
          <Typography variant="body1" sx={{ marginTop: "32px", marginBottom: "16px" }}>
            Captain
          </Typography>
          <Jurisdiction
            location={{
              latitude: unit.location?.latitude ?? -73.9249,
              longitude: unit.location?.longitude ?? 40.6943
            }}
          />
          <MostReportedOfficers
            reported_officers={unit.most_reported_officers}
            total_officers={unit.total_officers}
          />
          <Attachments />
        </>
      )
    },
    {
      label: "Officer List",
      content: <>Officer List</>,
      disabled: true
    },
    {
      label: "Complaint List",
      content: <>Complaints List</>,
      disabled: true
    },
    {
      label: "Insights",
      content: <>Insights</>,
      disabled: true
    }
  ]

  return <DetailsTabs tabs={tabs} ariaLabel="unit detail tabs" />
}
