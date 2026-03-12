"use client"

import { Typography } from "@mui/material"
import { Agency } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedUnits from "@/components/Details/MostReportedUnits"
import Attachments from "../Attachments"

export default function AgencyDetailsTabs(agency: Agency) {
  const tabs = [
    {
      label: "Overview",
      content: (
        <>
          <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
            Leadership
          </Typography>
          <Typography variant="body1" sx={{ marginTop: "32px", marginBottom: "16px" }}>
            Commissioner
          </Typography>
          <Jurisdiction
            location={{
              latitude: agency.location?.latitude ?? -73.9249,
              longitude: agency.location?.longitude ?? 40.6943
            }}
          />
          <MostReportedUnits
            most_reported_units={agency.most_reported_units}
            total_units={agency.total_units}
          />
          <Attachments />
        </>
      )
    },
    {
      label: "Unit List",
      content: <>Unit List</>,
      disabled: true
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

  return <DetailsTabs tabs={tabs} ariaLabel="agency detail tabs" />
}
