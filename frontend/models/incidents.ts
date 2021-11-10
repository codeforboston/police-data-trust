import { Incident } from "../helpers/api"
import { DepartmentType, OfficerRecordType } from "./officer"

/**
 * Expanded Incident Record
 */
export interface IncidentDetailType extends Incident {
  outcome: string[]
  location: string
  locationType: string
  locationGeo: number[]
  summary: string
  deptsInvolved: Array<DepartmentType>
  officersInvolved: Array<OfficerRecordType>
  incidentReportLink: string
  passportItems: string[]
}

// convert ["First Last", "First Last"] to ["F.Last, F.Last"]
export const formatOfficerNames = (officerNames: string[]): string => {
  const rx = /^(?<first>[A-Z])[a-z]+ (?<last>[A-Za-z]+)/
  const oNames = officerNames.map((str) => {
    const o = str.match(rx)
    return `${o.groups.first}.${o.groups.last}`
  })
  return oNames.join(", ")
}

export const formatDate = (unixTime: number): string => new Date(unixTime).toLocaleDateString()
