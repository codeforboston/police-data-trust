import { Column } from "react-table"
import { GreaterThanButton } from "../shared-components/icon-buttons/icon-buttons"

export interface IncidentRecordType {
  officers: string[]
  incidentType: string
  useOfForce: string[]
  source?: string
}

export const incidentResultsColumns: Column<any>[] = [
  {
    Header: "Officers involved",
    accessor: (row: any) => (Array.isArray(row["officers"]) ? row["officers"].join(", ") : ""),
    id: "officersInvolved"
  },
  {
    Header: "Incident Type",
    accessor: (row: any) => row["incidentType"],
    id: "incidentType"
  },
  {
    Header: "Use of Force",
    accessor: (row: any) => (Array.isArray(row["useOfForce"]) ? row["useOfForce"].join(", ") : ""),
    id: "useOfForce"
  },
  {
    Header: "Source",
    accessor: "source",
    id: "source"
  },
  {
    Header: "View Record",
    Cell: () => {
      return <GreaterThanButton title={"View Record"} onclick={() => console.log("clicked")} />
    },
    id: "record"
  }
]
