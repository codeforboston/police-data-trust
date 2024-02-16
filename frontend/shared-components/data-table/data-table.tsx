import { faArrowDown, faArrowUp } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React, { useState } from "react"
import { Column, useFilters, usePagination, useSortBy, useTable } from "react-table"
import { PageNavigator } from "./data-table-subcomps"
import styles from "./data-table.module.css"

interface DataTableProps<T extends object> {
  tableName: string
  columns: Column<T>[]
  data: T[] | undefined
}

export function DataTable<T extends object>(props: DataTableProps<T>) {
  const { data, columns } = props
  const { dataTable, dataHeader, dataRows } = styles

  const [editMode, setEditMode] = useState(false)
  const [showFilters, setShowFilters] = useState(false)

  const { tableWrapper, tableHeader, tableTitle, sortArrow, colFilter } = styles

  // TODO: When this gets changed from mocking to fetching the data from an api call, the 'full'
  // 'save' values will be appended to each item dynamically

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
  } = useTable<T>(
    {
      columns,
      data,
      initialState: { pageIndex: 0 }
    },
    useFilters,
    useSortBy,
    usePagination
  )

  function viewRecord(recordId: number) {
    // TODO: view full record
  }

  function toggleEditMode() {
    setEditMode(!editMode)
  }

  return (
    <>
      <div style={{ overflowX: "auto" }}>
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
      </div>
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
    </>
  )
}
