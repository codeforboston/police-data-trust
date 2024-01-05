import { faArrowDown, faArrowUp } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React, { useState } from "react"
import { Column, useFilters, usePagination, useSortBy, useTable } from "react-table"
import { PageNavigator } from "./officer-incident-data-table-subcomps"
import styles from "./officer-incident-data-table.module.css"
import { IncidentRecordType } from "../../models/incident"

interface OfficerIncidentDataTableProps {
  tableName: string
  columns: Column<any>[]
  data: IncidentRecordType[] | undefined
}

export function OfficerIncidentDataTable(props: OfficerIncidentDataTableProps) {
  const { data, columns } = props
  const { dataTable, dataHeader, dataRows } = styles
  const [showFilters, setShowFilters] = useState(false)

  const { sortArrow, colFilter } = styles

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
    <div>
      {/* <header className={tableHeader}></header> */}
      <table {...getTableProps()} className={dataTable} aria-label="Data Table">
        <thead className={dataHeader}>
          {headerGroups.map((headerGroup) => (
            // react-table prop types include keys, but eslint can't tell that
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
                    <div className={colFilter}>
                      {column.canFilter ? column.render("Filter") : null}
                    </div>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row)
            return (
              // eslint-disable-next-line react/jsx-key
              <tr {...row.getRowProps()} className={dataRows}>
                {row.cells.map((cell) => {
                  // eslint-disable-next-line react/jsx-key
                  return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                })}
              </tr>
            )
          })}
        </tbody>
      </table>

      <PageNavigator
        data={data}
        pageIndex={pageIndex}
        pageCount={pageCount}
        pageSize={pageSize}
        pageOptions={pageOptions}
        canPreviousPage={canPreviousPage}
        canNextPage={canNextPage}
        gotoPage={gotoPage}
        previousPage={previousPage}
        nextPage={nextPage}
        setPageSize={setPageSize}
      />
    </div>
  )
}
