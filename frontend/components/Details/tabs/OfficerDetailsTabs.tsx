"use client"

import { useMemo } from "react"
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
import { usePathname, useRouter, useSearchParams } from "next/navigation"

type OfficerDetailTab = "background" | "complaints" | "lawsuits" | "awards" | "attachments"

const DEFAULT_TAB: OfficerDetailTab = "background"
const ENABLED_TABS: OfficerDetailTab[] = ["background"]

const parseTab = (value: string | null): OfficerDetailTab => {
  if (value && ENABLED_TABS.includes(value as OfficerDetailTab)) {
    return value as OfficerDetailTab
  }

  return DEFAULT_TAB
}

export default function OfficerDetailsTabs(officer: Officer) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const activeTab = useMemo(() => parseTab(searchParams.get("tab")), [searchParams])

  const tabs = [
    {
      value: "background",
      label: "Background",
      content: (
        <StickySidebarLayout
          main={
            <>
              <Typography
                component="h2"
                variant="h5"
                sx={{ fontSize: "1.3rem", fontWeight: "500" }}
              >
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
      value: "complaints",
      label: "Complaints",
      content: <>Complaints</>,
      disabled: true
    },
    {
      value: "lawsuits",
      label: "Lawsuits",
      content: <>Lawsuits</>,
      disabled: true
    },
    {
      value: "awards",
      label: "Awards",
      content: <>Awards</>,
      disabled: true
    },
    {
      value: "attachments",
      label: "Attachments",
      content: <>Attachments</>,
      disabled: true
    }
  ]

  return (
    <DetailsTabs
      tabs={tabs}
      ariaLabel="officer detail tabs"
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
