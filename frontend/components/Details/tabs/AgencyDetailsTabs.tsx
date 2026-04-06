"use client"

import { useEffect, useState, useMemo } from "react"
import { Typography } from "@mui/material"
import { Agency, HasOfficers } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedUnits from "@/components/Details/MostReportedUnits"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import UnitList from "@/components/Details/UnitList"
import StickySidebarLayout from "@/components/Details/StickySidebarLayout"
import AgencyContentDetails from "@/components/Details/ContentDetails/AgencyContentDetails"
import { AgencyOfficerQueryParams, useAgencyOfficers } from "@/hooks/useAgencyOfficers"
import { useAgencyUnits } from "@/hooks/useAgencyUnits"
import { useOfficerListFilters } from "@/hooks/useOfficerListFilters"

export default function AgencyDetailsTabs(agency: Agency & HasOfficers) {
  const [activeTab, setActiveTab] = useState(0)
  const { filters: officerFilters, setFilters: setOfficerFilters } = useOfficerListFilters()
  const showOfficerList = activeTab === 2
  const showUnitList = activeTab === 1

  const {
    units,
    loading: unitsLoading,
    error: unitsError
  } = useAgencyUnits(agency.uid, showUnitList)

  const officerParams = useMemo<AgencyOfficerQueryParams>(
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
  } = useAgencyOfficers(agency.uid, showOfficerList, officerParams)

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
          }
          sidebar={<AgencyContentDetails agency={agency} />}
        />
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
      ariaLabel="agency detail tabs"
      value={activeTab}
      onChange={setActiveTab}
    />
  )
}
