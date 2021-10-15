import * as React from "react"
import { useTable, usePagination, useSortBy, useFilters } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPlusCircle, faSlidersH, faSave, faArrowUp, faArrowDown, faArrowCircleRight, faArrowAltCircleLeft } from "@fortawesome/free-solid-svg-icons"
import { InfoTooltip } from "../../shared-components"
import { TooltipIcons, TooltipTypes, IncidentTableData } from "../../models"

import styles from "./search-results.module.css"

// TODO: get API
let mockData: Array<IncidentTableData> = require("../../models/mock-data/grammy.json")

interface SearchResultsProps {
  incidents?: Array<IncidentTableData>
}

const resultsColumns = [
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
    Header: "Officer(s)",
    accessor: (row: any) => row["officers"].join(", "),
    id: "officers"
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
  },
]  



export default function SearchResultsTable({ incidents = mockData }: SearchResultsProps) {
  const { useState, useMemo } = React

  // TODO: display full record
  const fullRecord = (id: number) => { }

  const {
    dataTable,
    dataHeader,
    dataFooter,
    dataRowPage,
    dataRows,
    expandRecordButton
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
    useSortBy,
    usePagination
    
  )

  const [pageSizeValue, setPageSizeValue] = useState(pageSize)

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setPageSizeValue(+e.target.value)
  }

  function handleBlur(e: React.FocusEvent<HTMLInputElement>) {
    setPageSize(+e.target.value)
  }


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
                <span>
                  {column.isSorted 
                    ? column.isSortedDesc
                      ? <FontAwesomeIcon icon={faArrowDown} />
                      : <FontAwesomeIcon icon={faArrowUp} />
                    : ''
                    }
                </span>
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
                const { id } = cell.column
                if (id === "id") {
                  return (
                    <td>
                      <FontAwesomeIcon
                        className={expandRecordButton}
                        icon={faPlusCircle}
                        onClick={() => fullRecord(cell.value)}
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
          <td>{data.length.toLocaleString()} records found</td>
          <td colSpan={4}></td>
          <td>
            Show{" "}
            <input
              className={dataRowPage}
              min={1}
              max={10}
              onBlur={handleBlur}
              onChange={handleChange}
              type="number"
              value={pageSizeValue}
            />{" "}
            rows
          </td>
          <td>
            {" "}
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
              <FontAwesomeIcon icon={faArrowAltCircleLeft} />
            </button>{" "}
            {pageIndex + 1} of {pageOptions.length}{" "}
            <button onClick={() => nextPage()} disabled={!canNextPage}>
              <FontAwesomeIcon icon={faArrowCircleRight} />
            </button>{" "}
          </td>
        </tr>
      </tfoot>
    </table>
  )

}


