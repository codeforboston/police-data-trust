import { Column } from "react-table"
import { Incident, Perpetrator } from "../helpers/api"
import { CirclePlusButton } from "../shared-components/icon-buttons/icon-buttons"
import { InfoTooltip } from "../shared-components"
import { TooltipIcons, TooltipTypes } from "./info-tooltip"

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
  currentlyEmployed: boolean
  earliestEmployment: Date
  latestEmployment: Date
  badgeNumber?: string
}

export interface OfficerRecordType {
  recordId: number
  firstName: string
  lastName: string
  dateOfBirth?: Date
  gender?: string
  race?: string
  ethnicity?: string
  knownEmployers?: AgencyType[]
  workHistory?: EmploymentType[]
  accusations?: Perpetrator[]
  affiliations?: OfficerRecordType[]
}

export const officerResultsColumns: Column<any>[] = [
  {
    Header: "Name",
    accessor: (row: any) => `${row["first_name"]}, ${row["last_name"].charAt(0)}`,
    id: "name"
  },
  {
    Header: () => (
      <span>
        Allegations
        <InfoTooltip type={TooltipTypes.DATETIME} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: "allegations",
    id: "allegations"
  },
  {
    Header: "Race",
    accessor: "race",
    id: "race"
  },
  {
    Header: "Gender",
    accessor: "gender",
    id: "gender"
  },
  {
    Header: () => (
      <span>
        Rank
        <InfoTooltip type={TooltipTypes.DATETIME} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: "rank",
    id: "rank"
  },
  {
    Header: "Employers",
    accessor: "employers",
    id: "employers"
  },
  {
    Header: "Save",
    accessor: "save",
    Cell: () => {
      return <CirclePlusButton title={"Save"} onclick={() => console.log("clicked")} />
    },
    id: "save"
  }
]
