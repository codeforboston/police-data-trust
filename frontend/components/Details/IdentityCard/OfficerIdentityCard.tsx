import IdentityCard from "./IdentityCard"
import { Officer } from "@/utils/api"
import { US_STATES } from "@/utils/constants"

function getAgeFromBirthYear(yearOfBirth: string | number): number {
  return new Date().getFullYear() - Number(yearOfBirth)
}

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

function getOfficerFullName(officer: Officer): string {
  const middleName = officer.middle_name
    ? officer.middle_name.length === 1
      ? `${officer.middle_name}.`
      : officer.middle_name
    : null

  return [officer.first_name, middleName, officer.last_name].filter(Boolean).join(" ")
}

export default function OfficerIdentityCard(officer: Officer) {
  const currentEmployment = officer.employment_history?.find((emp) => !emp.latest_date)

  const subtitleParts = [
    officer.ethnicity,
    officer.gender ? officer.gender.toLowerCase() : null,
    officer.year_of_birth ? `${getAgeFromBirthYear(officer.year_of_birth)} years old` : null
  ].filter(Boolean)

  const detail = currentEmployment
    ? `${currentEmployment.highest_rank || "Officer"} at ${currentEmployment.agency_name}${
        currentEmployment.state ? `, ${getStateName(currentEmployment.state)}` : ""
      }`
    : undefined

  return (
    <IdentityCard
      title={getOfficerFullName(officer)}
      subtitle={subtitleParts.join(", ")}
      detail={detail}
    />
  )
}
