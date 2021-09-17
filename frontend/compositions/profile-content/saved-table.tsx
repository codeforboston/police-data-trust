import { IconDefinition } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import * as React from "react"
import { useTable, usePagination, Column } from "react-table"

import styles from "./saved.module.css"

interface SavedTableProps {
  itemTitle: string
  tableColumns: Array<any>
  tableData: Array<any>
  rowIdName: string
  expandIcon: IconDefinition
}

export default function SavedTable(props: SavedTableProps) {
  const { useState, useMemo } = React
  const [editMode, setEditMode] = useState(false)
  const { itemTitle, tableColumns, tableData, rowIdName, expandIcon } = props
  const {
    tableWrapper,
    tableHeader,
    tableTitle,
    editButton,
    editButtonOn,
    dataTable,
    dataHeader,
    dataFooter,
    dataRowPage,
    dataRows,
    expandRecordButton
  } = styles

  const data = useMemo(() => tableData, [tableData])
  const columns = useMemo(() => tableColumns, [tableColumns])

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

  function viewRecord(recordId: number) {
    // TODO: view full record
  }

  function toggleEditMode() {
    setEditMode(!editMode)
  }

  return (
    <div className={tableWrapper}>
      <header className={tableHeader}>
        <span className={tableTitle}>Saved {itemTitle}</span>
        <button className={editMode ? editButtonOn : editButton} onClick={toggleEditMode}>
          Edit {itemTitle}
        </button>
      </header>
      <table {...getTableProps()} className={dataTable} aria-label={`Saved ${itemTitle}`}>
        <thead className={dataHeader}>
          {headerGroups.map((headerGroup) => (
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
          {page.map((row) => {
            prepareRow(row)
            return (
              // eslint-disable-next-line react/jsx-key
              <tr {...row.getRowProps()} className={dataRows}>
                {row.cells.map((cell) => {
                  const { id } = cell.column
                  if (id === rowIdName) {
                    return (
                      <td>
                        <FontAwesomeIcon
                          className={expandRecordButton}
                          icon={expandIcon}
                          onClick={() => viewRecord(cell.value)}
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
