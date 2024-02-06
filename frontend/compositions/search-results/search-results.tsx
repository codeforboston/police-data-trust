import { Column } from "react-table"
import { faSlidersH } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

import { useSearch } from "../../helpers"
import { Incident, Officer, Perpetrator, Rank } from "../../helpers/api"
import { formatDate } from "../../helpers/syntax-helper"
import { TooltipIcons, TooltipTypes } from "../../models"
import { InfoTooltip } from "../../shared-components"
import { DataTable } from "../../shared-components/data-table/data-table"
import {
  CirclePlusButton,
  GreaterThanButton
} from "../../shared-components/icon-buttons/icon-buttons"

interface SearchProps {
  results: Incident[] | Officer[]
  resultsColumns: Column<any>[]
}

export default function SearchResultsTable(searchProps: SearchProps) {
  const { results, resultsColumns } = searchProps
  return (
    <>
      {!!searchProps.results.length ? (
        <DataTable tableName={"Search Results"} columns={resultsColumns} data={results} />
      ) : (
        <p>No Results</p>
      )}
    </>
  )
}

export const resultsColumns: Column<any>[] = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Perpetrator(s) Involved",
    accessor: (row: any) =>
      row["perpetrators"].map((names: Perpetrator) => Object.values(names).join(", ")).join(", "),
    filter: "text",
    id: "perpetrators"
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
    accessor: "incident_type",
    filter: "text"
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
    id: "use_of_force",
    filter: "text"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "Full",
    accessor: "full",
    Cell: (e) => (
      <a href={`/incident/${e.row.values.id}`}>
        <GreaterThanButton title={"Full"} onclick={() => console.log(e.row.values.id)} />
      </a>
    ),
    id: "full"
  },
  {
    Header: "Save",
    accessor: "save",
    Cell: () => {
      return <CirclePlusButton title={"Save"} onclick={() => console.log("clicked")} />
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
