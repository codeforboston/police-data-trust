import * as React from "react"

import { useTable } from "react-table"

type IncidentData = {
  dates: string
  incidentType: string
  officersInvolved: string[]
  subject: string
  source: string
}

export function DataTable() {
  // Defines table rows
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
    <table {...getTableProps()} style={{ border: "solid 1px blue" }}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th
                {...column.getHeaderProps()}
                style={{
                  borderBottom: "solid 3px red",
                  background: "aliceblue",
                  color: "black",
                  fontWeight: "bold",
                }}>
                {column.render("Header")}
              </th>
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
                return (
                  <td
                    {...cell.getCellProps()}
                    style={{
                      padding: "10px",
                      border: "solid 1px gray",
                      background: "papayawhip",
                    }}>
                    {cell.render("Cell")}
                  </td>
                )
              })}
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}
