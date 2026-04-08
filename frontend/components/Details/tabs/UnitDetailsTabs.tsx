"use client"

import { useEffect, useMemo } from "react"
import { Typography } from "@mui/material"
import { Unit, HasOfficers } from "@/utils/api"
import DetailsTabs from "./DetailsTabs"
import Jurisdiction from "../Jurisdiction"
import MostReportedOfficers from "@/components/Details/MostReportedOfficers"
import Attachments from "../Attachments"
import OfficerList from "@/components/Details/OfficerList"
import UnitContentDetails from "@/components/Details/ContentDetails/UnitContentDetails"
import StickySidebarLayout from "@/components/Details/StickySidebarLayout"
import { useDebouncedValue } from "@/hooks/useDebouncedValue"
import { UnitOfficerQueryParams, useUnitOfficers } from "@/hooks/useUnitOfficers"
import { useOfficerListFilters } from "@/hooks/useOfficerListFilters"
import { usePathname, useRouter, useSearchParams } from "next/navigation"

type UnitDetailTab = "overview" | "officers" | "complaints" | "insights"

const DEFAULT_TAB: UnitDetailTab = "overview"
const ENABLED_TABS: UnitDetailTab[] = ["overview", "officers"]

const parseTab = (value: string | null): UnitDetailTab => {
  if (value && ENABLED_TABS.includes(value as UnitDetailTab)) {
    return value as UnitDetailTab
  }

  return DEFAULT_TAB
}

export default function UnitDetailsTabs(unit: Unit & HasOfficers) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const activeTab = useMemo(() => parseTab(searchParams.get("tab")), [searchParams])
  const { filters: officerFilters, setFilters: setOfficerFilters } = useOfficerListFilters()
  const debouncedOfficerFilters = useDebouncedValue(officerFilters, 300)
  const showOfficerList = activeTab === "officers"

  const officerParams = useMemo<UnitOfficerQueryParams>(
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
  } = useUnitOfficers(unit.uid, showOfficerList, officerParams)

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
      value: "officers",
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
      ariaLabel="unit detail tabs"
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
