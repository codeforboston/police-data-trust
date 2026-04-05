export const EMPLOYMENT_TYPE_OPTIONS = ["Law Enforcement", "Corrections"] as const

export const EMPLOYMENT_STATUS_OPTIONS = [
  "Full-Time",
  "Part-Time",
  "Provisional",
  "Temporary",
  "Volunteer"
] as const

export const EMPLOYMENT_RANK_OPTIONS = [
  "Police Officer",
  "Detective",
  "Sergeant",
  "Lieutenant",
  "Captain",
  "Major",
  "Colonel",
  "Commander",
  "Chief"
] as const

export function formatEmploymentOptionLabel(value: string) {
  return value
    .toLowerCase()
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ")
}
