import * as React from "react"
import { formatDate } from "../../helpers/syntax-helper"
import { DataTable } from "../../shared-components/data-table/data-table"

export const searchesColumns = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Who",
    accessor: (row: any) => {
      row["who"].join(", ")
    },
    id: "who"
  },
  {
    Header: "What",
    accessor: "what"
  },
  {
    Header: "When",
    accessor: (row: any) => formatDate(row["when"]) || "when",
    id: "when"
  },
  {
    Header: "Where",
    accessor: "where"
  },
  {
    Header: "Results Total",
    accessor: "total"
  },
  {
    Header: "View Results",
    accessor: "results",
    disableSortBy: true
  }
]
export default function SavedTable() {
  const data: undefined = undefined
  // data will come from profile when that is built

  return <DataTable tableName={"Saved Records"} columns={searchesColumns} data={data} />
}
