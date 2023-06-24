import { Incident, Perpetrator } from "../helpers/api"

export interface AgencyType {
  agencyName: string
  agencyImage: string
  agencyHqAddress: string
  websiteUrl: string
}

export const agencyColumns = [
  {
    Header: "agency",
    accessor: "agency"
  },
  {
    Header: "Address",
    accessor: "agencyHqAddress"
  },
  {
    Header: "Website",
    accessor: "websiteUrl"
  },
  {
    Header: "Agency Address",
    accessor: "agencyHqAddress"
  }
]

export interface EmploymentType {
  agency: AgencyType
  currentlyEmployed: string
  earliestEmployment: Date
  latestEmployment: Date
  badgeNumber: string
}

export interface OfficerRecordType {
  recordId: number
  firstName: string
  lastName: string
  dateOfBirth?: Date
  gender?: string
  race?: string
  knownEmployers?: AgencyType[]
  workHistory: EmploymentType[]
  accusations?: Perpetrator[]
}
