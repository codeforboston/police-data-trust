"use client"

import { useEffect, useMemo, useState } from "react"
import { Typography } from "@mui/material"
import { Unit, HasOfficers } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedOfficers from "@/components/Details/MostReportedOfficers"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import UnitContentDetails from "@/components/Details/ContentDetails/UnitContentDetails"
import StickySidebarLayout from "@/components/Details/StickySidebarLayout"
import { UnitOfficerQueryParams, useUnitOfficers } from "@/hooks/useUnitOfficers"
import { useOfficerListFilters } from "@/hooks/useOfficerListFilters"

export default function UnitDetailsTabs(unit: Unit & HasOfficers) {
  const [activeTab, setActiveTab] = useState(0)
  const { filters: officerFilters, setFilters: setOfficerFilters } = useOfficerListFilters()
  const showOfficerList = activeTab === 1

  const officerParams = useMemo<UnitOfficerQueryParams>(
    () => ({
      term: officerFilters.searchTerm.trim() || undefined,
      rank: officerFilters.rank.length > 0 ? officerFilters.rank : undefined,
      status: officerFilters.status.length > 0 ? officerFilters.status : undefined,
      type: officerFilters.type.length > 0 ? officerFilters.type : undefined,
      include: ["employment"],
      page: 1,
      per_page: 25
    }),
    [officerFilters.rank, officerFilters.searchTerm, officerFilters.status, officerFilters.type]
  )

  const {
    officers,
    loading: officersLoading,
    error: officersError
  } = useUnitOfficers(unit.uid, showOfficerList, officerParams)

  useEffect(() => {
    if (officersError) {
      console.error("Failed to load officer list", officersError)
    }
  }, [officersError])

  const tabs = [
    {
      label: "Overview",
      content: (
        <StickySidebarLayout
          stickyTop="20px"
          main={
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
          }
          sidebar={<UnitContentDetails unit={unit} />}
        />
      )
    },
    {
      label: "Officer List",
      content: (
        <OfficerList
          org={unit}
          orgType="unit"
          officers={officers}
          loading={officersLoading}
          error={officersError}
          filters={officerFilters}
          onFiltersChange={setOfficerFilters}
          filterMode="hybrid"
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
