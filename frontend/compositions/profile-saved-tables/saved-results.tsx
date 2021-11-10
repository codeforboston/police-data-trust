import { faGreaterThan, faPlusCircle, faSlidersH } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"
import { Column } from "react-table"
import { useSearch } from "../../helpers"
import { Officer } from "../../helpers/api"
import { formatDate } from "../../helpers/syntax-helper"
import { TooltipIcons, TooltipTypes } from "../../models"
import { InfoTooltip } from "../../shared-components"
import { DataTable } from "../../shared-components/data-table/data-table"
import styles from "./saved.module.css"

export const savedResultsColumns: Column<any>[] = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Officer(s) Involved",
    accessor: (row: any) =>
      row["officers"].map((names: Officer) => Object.values(names).join(", ")).join(", "),
    id: "officers"
  },
  {
    Header: () => (
      <span className="columnHead">
        Date/Time
        <InfoTooltip type={TooltipTypes.DATETIME} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: (row: any) => new Date(row["occurred"]).toLocaleDateString(),
    id: "occurred"
  },
  {
    Header: "Incident Type",
    accessor: "incident_type"
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
    Header: "Full",
    accessor: "full",
    Cell: () => {
      return (
        <FontAwesomeIcon
          className={styles.actionBtn}
          title={"Full"}
          icon={faGreaterThan}
          onClick={() => console.log("clicked")}
        />
      )
    },
    id: "full"
  },
  {
    Header: "Save",
    accessor: "save",
    Cell: () => {
      return (
        <FontAwesomeIcon
          className={styles.actionBtn}
          title={"Full"}
          icon={faPlusCircle}
          onClick={() => console.log("clicked")}
        />
      )
    },
    id: "save"
  },
  {
    Header: () => (
      <span className="columnHeadIcon">
        <FontAwesomeIcon icon={faSlidersH} size="lg" />
      </span>
    ),
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
