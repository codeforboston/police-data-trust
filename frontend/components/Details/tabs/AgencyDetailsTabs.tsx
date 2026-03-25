"use client"

import { useEffect, useState } from "react"
import { Typography } from "@mui/material"
import { Agency } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedUnits from "@/components/Details/MostReportedUnits"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import { useUnitOfficers } from "@/hooks/useUnitOfficers"

export default function AgencyDetailsTabs(agency: Agency) {
  const [activeTab, setActiveTab] = useState(0)
  const showOfficerList = activeTab === 1
  console.log({ agencyUid: agency.uid })
  const {
    officers,
    loading: officersLoading,
    error: officersError
  } = useUnitOfficers(agency.uid, showOfficerList)

  console.log({ officers, officersLoading, officersError })
  useEffect(() => {
    if (officersError) {
      // eslint-disable-next-line no-console
      console.error("Failed to load officer list", officersError)
    }
  }, [officersError])

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
      content: (
        <OfficerList
          unit={agency}
          officers={officers}
          loading={officersLoading}
          error={officersError}
        />
      )
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

  return (
    <DetailsTabs
      tabs={tabs}
      ariaLabel="agency detail tabs"
      value={activeTab}
      onChange={setActiveTab}
    />
  )
}
