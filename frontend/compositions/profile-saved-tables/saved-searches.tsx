import React from "react"
import { Column } from "react-table"
import { useSearch } from "../../helpers"
import { Officer } from "../../helpers/api"
import { formatDate } from "../../helpers/syntax-helper"
import { TooltipIcons, TooltipTypes } from "../../models"
import { InfoTooltip } from "../../shared-components"
import { DataTable } from "../../shared-components/data-table/data-table"

// TODO: retrieve user saved searches from API

export const searchesColumns: Column<any>[] = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Date/Time",
    accessor: (row: any) => formatDate(row["time_of_incident"]),
    id: "time_of_incident"
  },
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
    Header: () => (
      <span className="columnHead">
        Use of Force
        <InfoTooltip type={TooltipTypes.USEFORCE} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
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
export default function SavedSearches() {
  const { incidentResults } = useSearch()
  // data will come from profile when that is built

  if (!incidentResults) return null
  if (incidentResults.results.length === 0) return <div>No results</div>

  return (
    <DataTable
      tableName={"Saved Searches"}
      columns={searchesColumns}
      data={incidentResults.results}
    />
  )
}
