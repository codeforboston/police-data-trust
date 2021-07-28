import * as React from "react"

import { useTable } from "react-table"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faGreaterThan, faPlusCircle, IconDefinition } from "@fortawesome/free-solid-svg-icons"

import styles from "./data-table.module.css"

export function DataTable({ count = 220375 }) {
  const { useMemo, useState } = React;
  const { dataTable, dataHeader, dataFooter, dataRowPage, dataRows, dataRow } = styles
  const [rowsShown, setRowsShown] = useState(7)

  // TODO: Move to models
  interface IncidentData {
    dates: string
    incidentType: string
    officersInvolved: string[]
    subject: IconDefinition
    source: IconDefinition
  }

  // TODO: When this gets changed from mocking to fetching the data from an api call, the 'full'
  // 'save' values will be appended to each item dynamically
  const data = useMemo(
    () => [
      {
        dates: "2003/01/01",
        incidentType: "Use of force",
        officersInvolved: ["Dan Smith"],
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
        officersInvolved: ["Ed Smith, Vince Gilligan"],
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
        officersInvolved: ["Dan Smith"],
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
        officersInvolved: ["Ed Smith, Vince Gilligan"],
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
    <div>
      <table {...getTableProps()} className={dataTable} aria-label="Search Results Table">
        <thead className={dataHeader}>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()} >
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
              <tr {...row.getRowProps()} className={dataRows}>
                {row.cells.map((cell) => {
                  const { id } = cell.column
                  if (id === "full" || id === "save") {
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
        <tfoot className={dataFooter}>
          <tr>
            <td>{count.toLocaleString()} records found</td>
              <td colSpan={4}></td>
              <td>
                Show <span className={dataRowPage}>{rowsShown}</span> rows
              </td>
              <td>&lt; 1 of 31,482 &gt;</td>
          </tr>
        </tfoot>
      </table>
    </div>
  )
}
