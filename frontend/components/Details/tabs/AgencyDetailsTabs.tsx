"use client"

import { useEffect, useMemo } from "react"
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
import { useDebouncedValue } from "@/hooks/useDebouncedValue"
import { useOfficerListFilters } from "@/hooks/useOfficerListFilters"
import { usePathname, useRouter, useSearchParams } from "next/navigation"

type AgencyDetailTab = "overview" | "units" | "officers" | "complaints" | "insights"

const DEFAULT_TAB: AgencyDetailTab = "overview"
const ENABLED_TABS: AgencyDetailTab[] = ["overview", "units", "officers"]

const parseTab = (value: string | null): AgencyDetailTab => {
  if (value && ENABLED_TABS.includes(value as AgencyDetailTab)) {
    return value as AgencyDetailTab
  }

  return DEFAULT_TAB
}

export default function AgencyDetailsTabs(agency: Agency & HasOfficers) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const activeTab = useMemo(() => parseTab(searchParams.get("tab")), [searchParams])
  const { filters: officerFilters, setFilters: setOfficerFilters } = useOfficerListFilters()
  const debouncedOfficerFilters = useDebouncedValue(officerFilters, 300)
  const showOfficerList = activeTab === "officers"
  const showUnitList = activeTab === "units"

  const {
    units,
    loading: unitsLoading,
    error: unitsError
  } = useAgencyUnits(agency.uid, showUnitList)

  const officerParams = useMemo<AgencyOfficerQueryParams>(
    () => ({
      term: debouncedOfficerFilters.searchTerm.trim() || undefined,
      rank: debouncedOfficerFilters.rank.length > 0 ? debouncedOfficerFilters.rank : undefined,
      status:
        debouncedOfficerFilters.status.length > 0 ? debouncedOfficerFilters.status : undefined,
      type: debouncedOfficerFilters.type.length > 0 ? debouncedOfficerFilters.type : undefined,
      include: ["employment"],
      page: 1,
      per_page: 25
    }),
    [
      debouncedOfficerFilters.rank,
      debouncedOfficerFilters.searchTerm,
      debouncedOfficerFilters.status,
      debouncedOfficerFilters.type
    ]
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
      value: "overview",
      label: "Overview",
      content: (
        <StickySidebarLayout
          main={
            <>
              <Typography
                component="h2"
                variant="h5"
                sx={{ fontSize: "1.3rem", fontWeight: "500" }}
              >
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
      value: "units",
      label: "Unit List",
      content: <UnitList agency={agency} units={units} loading={unitsLoading} error={unitsError} />
    },
    {
      value: "officers",
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
      value: "complaints",
      label: "Complaint List",
      content: <>Complaints List</>,
      disabled: true
    },
    {
      value: "insights",
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
      onChange={(newValue) => {
        const nextTab = parseTab(String(newValue))
        const nextParams = new URLSearchParams(searchParams.toString())

        if (nextTab === DEFAULT_TAB) {
          nextParams.delete("tab")
        } else {
          nextParams.set("tab", nextTab)
        }

        const destination = nextParams.toString()
        router.push(destination ? `${pathname}?${destination}` : pathname)
      }}
    />
  )
}
