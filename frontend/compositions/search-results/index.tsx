import * as React from "react"
import { useTable, usePagination, useSortBy, useFilters } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPlusCircle, faSlidersH, faSave, faArrowUp, faArrowDown, faAngleRight, faAngleLeft, faAngleDoubleRight, faAngleDoubleLeft } from "@fortawesome/free-solid-svg-icons"
import { InfoTooltip } from "../../shared-components"
import { TooltipIcons, TooltipTypes, IncidentTableData } from "../../models"

import styles from "./search-results.module.css"

// TODO: get API
let mockData: Array<IncidentTableData> = require("../../models/mock-data/grammy.json")


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

interface SearchResultsProps {
  incidents?: Array<IncidentTableData>
}
export default function SearchResultsTable({ incidents = mockData }: SearchResultsProps) {
  const { useState, useMemo } = React
  
  const [showFilters, setShowFilters] = useState(false)

  // TODO: display full record
  const fullRecord = (id: number) => { }
  
  // TODO: save record
  const saveRecord = (id: number) => { }


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
    <>
    <table {...getTableProps()} className={dataTable} aria-label="Search Results">
      <thead className={dataHeader}>
        {headerGroups.map((headerGroup) => (
          // eslint-disable-next-line react/jsx-key
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              // eslint-disable-next-line react/jsx-key
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {column.render("Header")}
                <span className={sortArrow} >
                  {column.isSorted 
                    ? column.isSortedDesc
                      ? <FontAwesomeIcon icon={faArrowDown} />
                      : <FontAwesomeIcon icon={faArrowUp} />
                    : ' '
                    }
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
    </table>

    <div className={dataFooter}>
      <span className={recordCount}>Found {data.length.toLocaleString()} records</span>
      <button className={pageBtn} onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
        <FontAwesomeIcon icon={faAngleDoubleLeft} />
      </button>
      <button className={pageBtn} onClick={() => previousPage()} disabled={!canPreviousPage}>
        <FontAwesomeIcon icon={faAngleLeft} />
      </button>
      <span className={pageCnt}>Page <strong>{pageIndex + 1}</strong> of <strong>{pageOptions.length}</strong>{" "}</span>
      <button className={styles.pageBtn} onClick={() => nextPage()} disabled={!canNextPage}>
        <FontAwesomeIcon icon={faAngleRight} />
      </button>
      <button className={pageBtn} onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage} >
        <FontAwesomeIcon icon={faAngleDoubleRight} />
      </button>
      <span className={goto}>Go to page:{" "}
        <input type="number" className={dataRowPage} defaultValue={pageIndex + 1} 
          onChange={e => {
            const page = e.target.value ? Number(e.target.value) - 1 : 0
            gotoPage(page)
          }} 
          style={{ width: "50px", textAlign: "right" }} />
      </span>{" "}
      <select value={pageSize} onChange={e => setPageSize(Number(e.target.value))}>
        {[10, 20, 30, 40, 50].map(pageSize => (
          <option key={pageSize} value={pageSize}>
            Show {pageSize}
          </option>
        ))}
      </select>
    </div>
    </>
  )

}


