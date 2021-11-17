import { Incident } from "../helpers/api"

export interface DepartmentType {
  departmentName: string
  deptImage: string
  deptAddress: string
  webAddress: string
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

export interface EmploymentType {
  department: DepartmentType
  status: string
  startDate: Date
  endDate: Date
}

export interface OfficerRecordType {
  recordId: number
  firstName: string
  lastName: string
  badgeNo: string
  status: string
  department: string
  birthDate?: Date
  gender?: string
  race?: string
  ethnicity?: string
  incomeBracket?: string
  workHistory: EmploymentType[]
  affiliations?: string[]
  incidents?: Incident[]
}
