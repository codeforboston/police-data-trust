import Link from "next/link"
import { Link as MuiLink } from "@mui/material"
import IdentityCard from "./IdentityCard"
import { Unit } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

type UnitIdentityCardProps = {
  unit: Unit
}

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

export default function UnitIdentityCard({ unit }: UnitIdentityCardProps) {
  const location =
    unit.location?.city && unit.location?.state
      ? ` - ${unit.location.city}, ${getStateName(unit.location.state)}`
      : ""

  const title = `${unit.name}${location}`
  const subtitle =
    unit.agency?.uid && unit.agency?.name ? (
      <>
        Unit of{" "}
        <MuiLink
          component={Link}
          href={`/agency/${unit.agency.uid}`}
          underline="none"
          color="inherit"
          sx={{
            transition: "color 160ms ease",
            "&:hover": {
              color: "primary.main"
            }
          }}
        >
          {unit.agency.name}
        </MuiLink>
      </>
    ) : (
      `Unit of ${unit.agency?.name ?? "Unknown Agency"}`
    )
  const detail =
    unit.total_officers !== undefined
      ? `${unit.total_officers} known officers`
      : "Officer count not available"

  return <IdentityCard title={title} subtitle={subtitle} detail={detail} />
}
