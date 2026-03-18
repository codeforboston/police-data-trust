"use client"

import { useEffect, useState } from "react"
import { Typography } from "@mui/material"
import { Unit } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedOfficers from "@/components/Details/MostReportedOfficers"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import { useUnitOfficers } from "@/hooks/useUnitOfficers"

export default function UnitDetailsTabs(unit: Unit) {
  const [activeTab, setActiveTab] = useState(0)
  const showOfficerList = activeTab === 1

  const { officers, loading: officersLoading, error: officersError } = useUnitOfficers(
    unit.uid,
    showOfficerList
  )

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
      content: (
        <OfficerList
          unit={unit}
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
      ariaLabel="unit detail tabs"
      value={activeTab}
      onChange={setActiveTab}
    />
  )
}
