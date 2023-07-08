import { Incident } from "../helpers/api"

export interface AgencyType {
  agencyName: string
  agencyImage: string
  agencyHqAddress: string
  websiteUrl: string
}

export const departmentColumns = [
  {
    Header: "Department",
    accessor: "dept"
  },
  {
    Header: "Address",
    accessor: "deptAddress"
  },
  {
    Header: "Website",
    accessor: "webAddress"
  },
  {
    Header: "Dept Address",
    accessor: "deptAddress"
  }
]

export interface PerpetratorRecordType {
  recordId: number
  firstName?: string
  lastName?: string
  badge?: string
  rank?: string
  gender?: string
  race?: string
  ethnicity?: string
  incident?: Incident
}
