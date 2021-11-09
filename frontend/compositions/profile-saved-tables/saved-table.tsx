import * as React from "react"
import { useMemo } from "react"
import { Column } from "react-table"
import { resultsColumns, SavedResultsType } from "../../models"
import { DataTable } from "../../shared-components/data-table/data-table"

interface SavedTableProps {
  itemTitle?: string
  tableData: SavedResultsType[] 
}

export default function SavedTable(props: SavedTableProps) {
  const { tableData } = props

  const data = useMemo(() => tableData, [])
  const columns = useMemo(() => resultsColumns, []) as Column<any>[]

  return <DataTable tableName={"Saved Records"} tableColumns={columns} tableData={data} />
}
