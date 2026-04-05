"use client"

import { useEffect, useState } from "react"
import { Typography } from "@mui/material"
import { Agency, HasOfficers } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedUnits from "@/components/Details/MostReportedUnits"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import UnitList from "@/components/Details/UnitList"
import { useUnitOfficers } from "@/hooks/useUnitOfficers"
import { useAgencyUnits } from "@/hooks/useAgencyUnits"

export default function AgencyDetailsTabs(agency: Agency & HasOfficers) {
  const [activeTab, setActiveTab] = useState(0)
  const showOfficerList = activeTab === 2
  const showUnitList = activeTab === 1

  const {
    units,
    loading: unitsLoading,
    error: unitsError
  } = useAgencyUnits(agency.uid, showUnitList)

  const {
    officers,
    loading: officersLoading,
    error: officersError
  } = useUnitOfficers(agency.uid, showOfficerList)

  useEffect(() => {
    if (officersError) {
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
      content: <UnitList agency={agency} units={units} loading={unitsLoading} error={unitsError} />
    },
    {
      label: "Officer List",
      content: (
        <OfficerList
          org={agency}
          orgType="agency"
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
