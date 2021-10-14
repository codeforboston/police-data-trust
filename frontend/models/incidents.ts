import { DepartmentType , OfficerRecordType } from "./officer"

/**
 * Data to appear in Incidents table
 * full record will be superset
 */
 export interface IncidentTableData {
  id: number,
  occurred: number, // UNIX timestamp
  officers: string[],   // officer names, "F.Last" (first initial, last name)
  incidentType: string,
  useOfForce: string[],
  source: string
}


/**
 * Expanded Incident Record
 */
export interface IncidentDetailType extends IncidentTableData {
  outcome: string[],
  location: string,
  locationType: string,
  locationGeo: number[],
  summary: string,
  deptsInvolved: Array<DepartmentType>,
  officersInvolved: Array<OfficerRecordType>,
  incidentReportLink: string,
  passportItems: string[]
}


// Incident Table Data
export const incidentsColumns = [
  {
    Header: "Date/Time",
    accessor: (row: any) => formatDate(row["occurred"]),
    id: "occurred"
  },
  {
    Header: "Officer(s)",
    accessor: (row: any) => row["officers"].join(", "),
    id: "officers"
  },
  {
    Header: "Incident Type",
    accessor: "incidentType"
  },
  {
    Header: "Use of Force",
    accessor: (row: any) => row["useOfForce"].join(", "),
    id: "useOfForce"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "#",
    accessor: "id",
    disableSortBy: true
  },
]

// convert ["First Last", "First Last"] to ["F.Last, F.Last"]
export const formatOfficerNames = (officerNames: string[]): string => {
  const rx = /^(?<first>[A-Z])[a-z]+ (?<last>[A-Za-z]+)/
  const oNames = officerNames.map(str => {
    const o = str.match(rx)
    return `${o.groups.first}.${o.groups.last}`
  })
  return oNames.join(", ")
}



export const formatDate = (unixTime: number): string => new Date(unixTime).toLocaleDateString()