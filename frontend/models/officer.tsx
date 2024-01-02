import { Column } from "react-table"
import { Perpetrator } from "../helpers/api"
import { CirclePlusButton, GreaterThanButton } from "../shared-components/icon-buttons/icon-buttons"
import { InfoTooltip } from "../shared-components"
import { TooltipIcons, TooltipTypes } from "./info-tooltip"
import Link from "next/link"
import { AppRoutes } from "./app-routes"
import { IncidentRecordType } from "./incident"

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
  badgeNo?: string
  status?: string
  department?: string
  knownEmployers?: AgencyType[]
  workHistory?: EmploymentType[]
  accusations?: Perpetrator[]
  affiliations?: string[]
  incidents?: IncidentRecordType[]
}

export const officerResultsColumns: Column<any>[] = [
  {
    Header: "Name",
    accessor: (row: any) => (
      <Link href={`${AppRoutes.OFFICER}/${row["recordId"]}`} passHref={true}>
        <div>{`${row["firstName"]}, ${row["lastName"]}`}</div>
      </Link>
    ),
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
    accessor: "status",
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
