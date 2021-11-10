import * as React from "react"
import { Column } from "react-table"
import { useSearch } from "../../helpers"
import { Officer } from "../../helpers/api"
import { formatDate } from "../../helpers/syntax-helper"
import { DataTable } from "../../shared-components/data-table/data-table"

export const resultsColumns: Column<any>[] = [
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

export default function SearchResultsTable() {
  const { incidentResults } = useSearch()

  if (!incidentResults) return null
  if (incidentResults.results.length === 0) return <div>No results</div>

  return (
    <DataTable
      tableName={"Search Results"}
      columns={resultsColumns}
      data={incidentResults.results}
    />
  )
}
