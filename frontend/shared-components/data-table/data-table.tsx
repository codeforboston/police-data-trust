import * as React from "react"

import { useTable } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faGreaterThan, faPlusCircle } from "@fortawesome/free-solid-svg-icons"

import styles from "./data-table.module.css"

type IncidentData = {
  dates: string
  incidentType: string
  officersInvolved: string[]
  subject: string
  source: string
}

export function DataTable({ count = 220375 }) {
  // Defines table rows
  const { dTable, dHeader, dFooter, dPagContainer, dRowPage, dTableWrapper } = styles
  const [rowsShown, setRowsShown] = React.useState(7)

  // TODO: When this gets changed from mocking to fetching the data from an api call, append
  // the
  const data = React.useMemo(
    () => [
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
        full: faGreaterThan,
        save: faPlusCircle,
      },
    ],
    []
  )

  const columns = React.useMemo(
    () => [
      {
        Header: "Date(s)",
        accessor: "dates" as const,
      },
      {
        Header: "Incident Type",
        accessor: "incidentType" as const,
      },
      {
        Header: "Officer(s) Involved",
        accessor: "officersInvolved" as const,
      },
      {
        Header: "Subject",
        accessor: "subject" as const,
      },
      {
        Header: "Source",
        accessor: "source" as const,
      },
      {
        Header: "Full Record",
        accessor: "full" as const,
      },
      {
        Header: "Save Record",
        accessor: "save" as const,
      },
    ],
    []
  )
  const tableInstance = useTable({ columns, data })

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance

  return (
    <div className={dTableWrapper}>
      <table {...getTableProps()} className={dTable}>
        <thead className={dHeader}>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => {
                  console.log(cell)
                  if (cell.column.id === "full" || cell.column.id === "save") {
                    return (
                      <td>
                        <FontAwesomeIcon icon={cell.value} />
                      </td>
                    )
                  }
                  return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                })}
              </tr>
            )
          })}
        </tbody>
        <tfoot className={dFooter}>
          <tr>
            <td>{count.toLocaleString()} records found</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>
              Show <span className={dRowPage}>{rowsShown}</span> rows
            </td>
            <td>&lt; 1 of 31,482 &gt;</td>
          </tr>
        </tfoot>
      </table>
      </div>
  )
}
