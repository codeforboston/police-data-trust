import IdentityCard from "./IdentityCard"
import { Unit } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

export default function UnitIdentityCard(unit: Unit) {

  return (
    <IdentityCard
      title={unit.name}
      subtitle={"Coming soon"}
      detail={"Coming soon"}
    />
  )
}
