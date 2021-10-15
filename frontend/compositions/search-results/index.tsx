import * as React from "react"
import { useTable, usePagination, useSortBy, useFilters } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import {
  faPlusCircle,
  faSlidersH,
  faSave,
  faArrowUp,
  faArrowDown,
  faAngleRight,
  faAngleLeft
} from "@fortawesome/free-solid-svg-icons"
import { InfoTooltip } from "../../shared-components"
import { TooltipIcons, TooltipTypes, IncidentTableData } from "../../models"

import styles from "./search-results.module.css"

// TODO: get API
let mockData: Array<IncidentTableData> = require("../../models/mock-data/grammy.json")

const resultsColumns = [
  {
    Header: "Officer(s) Involved",
    accessor: (row: any) => row["officers"].join(", "),
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
    accessor: "incidentType"
  },
  {
    Header: () => (
      <span className="columnHead">
        Use of Force
        <InfoTooltip type={TooltipTypes.USEFORCE} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: (row: any) => row["useOfForce"].join(", "),
    id: "useOfForce"
  },
  {
    Header: "Source",
    accessor: "source"
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

interface SearchResultsProps {
  incidents?: Array<IncidentTableData>
}
export default function SearchResultsTable({ incidents = mockData }: SearchResultsProps) {
  const { useState, useMemo } = React

  const [showFilters, setShowFilters] = useState(false)

  // TODO: display full record
  const fullRecord = (id: number) => {}

  // TODO: save record
  const saveRecord = (id: number) => {}

  const {
    dataTable,
    dataHeader,
    dataFooter,
    dataRowPage,
    dataRows,
    actionBtn,
    pageBtn,
    sortArrow,
    recordCount,
    pageCnt,
    goto
  } = styles

  const data = useMemo(() => incidents, [incidents])
  const columns = useMemo(() => resultsColumns, [])

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize }
  } = useTable(
    {
      columns,
      data,
      initialState: { pageIndex: 0 }
    },
    useFilters,
    useSortBy,
    usePagination
  )

  return (
      <table {...getTableProps()} className={dataTable} aria-label="Search Results">
        <thead className={dataHeader}>
          {headerGroups.map((headerGroup) => (
            // eslint-disable-next-line react/jsx-key
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                // eslint-disable-next-line react/jsx-key
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render("Header")}
                  <span className={sortArrow}>
                    {column.isSorted ? (
                      column.isSortedDesc ? (
                        <FontAwesomeIcon icon={faArrowDown} />
                      ) : (
                        <FontAwesomeIcon icon={faArrowUp} />
                      )
                    ) : (
                      "  "
                    )}
                  </span>
                  {showFilters && (
                    <div className={styles.colFilter}>
                      {column.canFilter ? column.render("Filter") : null}
                    </div>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row) => {
            prepareRow(row)
            return (
              // eslint-disable-next-line react/jsx-key
              <tr {...row.getRowProps()} className={dataRows}>
                {row.cells.map((cell) => {
                  if (cell.column.id === "id") {
                    return (
                      <td>
                        <FontAwesomeIcon
                          className={actionBtn}
                          title="Save Record"
                          icon={faPlusCircle}
                          onClick={() => saveRecord(cell.value)}
                        />
                      </td>
                    )
                  }
                  return (
                    // eslint-disable-next-line react/jsx-key
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>
        <tfoot className={dataFooter}>
          <tr>
            <td className={recordCount}>
              <strong>{data.length.toLocaleString()} records found</strong>
            </td>
            <td colSpan={2} />
            <td colSpan={2}>
              <button className={pageBtn} onClick={() => previousPage()} disabled={!canPreviousPage}>
                <FontAwesomeIcon icon={faAngleLeft} />
              </button>
              <span className={pageCnt}>
                {pageIndex + 1} of {pageOptions.length}
              </span>
              <button className={pageBtn} onClick={() => nextPage()} disabled={!canNextPage}>
                <FontAwesomeIcon icon={faAngleRight} />
              </button>
            </td>
            <td />
          </tr>
        </tfoot>

      </table>
  )
}
