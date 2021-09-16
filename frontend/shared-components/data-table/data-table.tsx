import * as React from "react"

import { useTable, usePagination } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

import { mockData, tableColumns } from "../../models/mock-data/mock-table-data"
import styles from "./data-table.module.css"

export function DataTable() {
  const icons = ["full", "save"]
  const { useMemo, useState } = React
  const { dataTable, dataHeader, dataFooter, dataRowPage, dataRows } = styles

  // TODO: When this gets changed from mocking to fetching the data from an api call, the 'full'
  // 'save' values will be appended to each item dynamically
  const data = useMemo(() => mockData, [])

  const columns = React.useMemo(() => tableColumns, [])

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
    <div>
      <table {...getTableProps()} className={dataTable} aria-label="Search Results Table">
        <thead className={dataHeader}>
          {headerGroups.map((headerGroup) => (
            // react-table prop types include keys, but eslint can't tell that
            // eslint-disable-next-line react/jsx-key
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                // eslint-disable-next-line react/jsx-key
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
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
                  const { id } = cell.column
                  if (icons.includes(id)) {
                    return (
                      <td>
                        <FontAwesomeIcon icon={cell.value} />
                      </td>
                    )
                  }
                  // eslint-disable-next-line react/jsx-key
                  return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
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
                {"<"}
              </button>{" "}
              {pageIndex + 1} of {pageOptions.length}{" "}
              <button onClick={() => nextPage()} disabled={!canNextPage}>
                {">"}
              </button>{" "}
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  )
}
