"use client"

import { Typography } from "@mui/material"
import { Officer } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Employment from "../Employment"
import AllegationsSummary from "../AllegationsSummary"
import StateRecords from "../StateRecords"
import Lawsuits from "../Lawsuits"
import Awards from "../Awards"
import Attachments from "../Attachments"
import OfficerContentDetails from "@/components/Details/ContentDetails/OfficerContentDetails"
import StickySidebarLayout from "@/components/Details/StickySidebarLayout"

export default function OfficerDetailsTabs(officer: Officer) {
  const tabs = [
    {
      label: "Background",
      content: (
        <StickySidebarLayout
          stickyTop="20px"
          main={
            <>
            <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
              Background
            </Typography>
            <StateRecords officer={officer} />
            <Employment employment_history={officer.employment_history} />
            <AllegationsSummary allegation_summary={officer.allegation_summary} />
            <Lawsuits />
            <Awards />
            <Attachments />
            </>
          }
          sidebar={<OfficerContentDetails officer={officer} />}
        />
      )
    },
    {
      label: "Complaints",
      content: <>Complaints</>,
      disabled: true
    },
    {
      label: "Lawsuits",
      content: <>Lawsuits</>,
      disabled: true
    },
    {
      label: "Awards",
      content: <>Awards</>,
      disabled: true
    },
    {
      label: "Attachments",
      content: <>Attachments</>,
      disabled: true
    }
  ]

  return <DetailsTabs tabs={tabs} ariaLabel="officer detail tabs" />
}
