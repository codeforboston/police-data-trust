import IdentityCard from "./IdentityCard"
import { Agency } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

function getAgencyLocation(agency: Agency): string | undefined {
  const parts = [agency.hq_city, agency.hq_state ? getStateName(agency.hq_state) : null].filter(
    Boolean
  )

  return parts.length > 0 ? parts.join(", ") : undefined
}

function getAgencyDetail(agency: Agency): string | undefined {
  if (agency.jurisdiction) return agency.jurisdiction
  if (agency.description) return agency.description
  if (agency.website_url) return agency.website_url
  return undefined
}

export default function AgencyIdentityCard(agency: Agency) {
  return (
    <IdentityCard
      title={agency.name}
      subtitle={getAgencyLocation(agency)}
      detail={getAgencyDetail(agency)}
    />
  )
}
