import IdentityCard from "./IdentityCard"
import { Unit } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

export default function UnitIdentityCard(unit: Unit) {
  const titleStr =
    unit.name +
    (unit.location && unit.location.city && unit.location.state
      ? ` - ${unit.location.city}, ${getStateName(unit.location.state)}`
      : "")

  const subtitlestr = "Unit of " + (unit.agency ? unit.agency.name : "Unknown Agency")

  const detailStr =
    unit.total_officers !== undefined
      ? `${unit.total_officers} known officers`
      : "Officer count not available"

  return <IdentityCard title={titleStr} subtitle={subtitlestr} detail={detailStr} />
}
