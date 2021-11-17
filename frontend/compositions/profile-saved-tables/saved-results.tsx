import React from "react"
import { Column } from "react-table"
import { useSearch } from "../../helpers"
import { Officer } from "../../helpers/api"
import { DataTable } from "../../shared-components/data-table/data-table"

export const savedResultsColumns: Column<any>[] = [
  {
    Header: "Officer(s)",
    accessor: (row: any) =>
      row["officers"].map((names: Officer) => Object.values(names).join(", ")).join(", "),
    id: "officers"
  },
  {
    Header: "Department",
    accessor: "department"
  },
  {
    Header: "Use of Force",
    accessor: (row: any) =>
      row["use_of_force"].map((items: string) => Object.values(items).join(", ")).join(", "),
    id: "use_of_force"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "View",
    accessor: "id",
    disableSortBy: true
  }
]

export default function SavedResults() {
  const { incidentResults } = useSearch()
  // data will come from profile when that is built

  if (!incidentResults) return null
  if (incidentResults.results.length === 0) return <div>No results</div>

  return (
    <DataTable
      tableName={"Saved Records"}
      columns={savedResultsColumns}
      data={incidentResults.results}
    />
  )
}
