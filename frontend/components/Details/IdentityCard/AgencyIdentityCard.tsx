import IdentityCard from "./IdentityCard"
import { Agency } from "@/utils/api"
import { US_STATES } from "@/utils/constants"
import type { ReactNode } from "react"
import Link from "@mui/material/Link"

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

function getAgencySubtitle(agency: Agency): string | undefined {
  const locationParts = [
    agency.hq_city,
    agency.hq_state ? getStateName(agency.hq_state) : null
  ].filter(Boolean)

  if (!agency.jurisdiction) return undefined

  if (agency.jurisdiction.toLowerCase() === "municipal") {
    return `Municipal Police Department${
      locationParts.length > 0 ? ` - ${locationParts.join(", ")}` : ""
    }`
  }

  return locationParts.length > 0 ? `Headquartered in ${locationParts.join(", ")}` : undefined
}

function getAgencyDetail(agency: Agency): ReactNode {
  const officers = agency.total_officers ?? "No"
  const units = agency.total_units ?? "No"
  const complaints = agency.total_complaints ?? "No"

  return (
    <>
      {officers} known officers, {units} known units, and {complaints} registered complaints
      {agency.website_url && (
        <>
          <br />
          Website:{" "}
          <Link href={agency.website_url} target="_blank" rel="noopener noreferrer">
            Visit website
          </Link>
        </>
      )}
    </>
  )
}

type AgencyIdentityCardProps = {
  agency: Agency
}

export default function AgencyIdentityCard({ agency }: AgencyIdentityCardProps) {
  return (
    <IdentityCard
      title={agency.name}
      subtitle={getAgencySubtitle(agency)}
      detail={getAgencyDetail(agency)}
    />
  )
}
