import { IconDefinition } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faArrowUp, faArrowDown, faAngleRight, faAngleLeft, faAngleDoubleRight, faAngleDoubleLeft } from "@fortawesome/free-solid-svg-icons"
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
    pageBtn,
    actionBtn,
    sortArrow,
    recordCount, 
    pageCnt,
    goto
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
                  if (cell.column.id === rowIdName) {
                    return (
                      <td>
                        <FontAwesomeIcon
                          className={actionBtn}
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
    </div>
  )
}
