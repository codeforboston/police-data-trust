import * as React from "react"

import { useTable } from "react-table"

import styles from './data-table.module.css';

type IncidentData = {
  dates: string
  incidentType: string
  officersInvolved: string[]
  subject: string
  source: string
}

export function DataTable({ count = 220375}) {
  // Defines table rows
  const { dTable, dHeader, dFooter, dPagContainer } = styles;
  const [rowsShown, setRowsShown] = React.useState(7);
  const data = React.useMemo(
    () => [
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
      },
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["John Smith"],
        subject: "unknown",
        source: "News Article",
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
    ],
    []
  )
  const tableInstance = useTable({ columns, data })

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance

  return (
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
                return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
              })}
            </tr>
          )
        })}
      </tbody>
      <tfoot className={dFooter}>
        <span>{count} records found</span>
        <div className={dPagContainer}>
          <p>Show <span>{rowsShown}</span> rows</p>
        </div>
      </tfoot>
    </table>
  )
}
