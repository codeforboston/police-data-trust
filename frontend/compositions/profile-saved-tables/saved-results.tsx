import React, { useMemo } from "react"
import { Column } from "react-table"
import { resultsColumns, SavedResultsType } from "../../models/saved-table"
import { DataTable } from "../../shared-components/data-table/data-table"

interface SavedResultsProps {
  tableData?: SavedResultsType[]
}

export default function SavedResults(props: SavedResultsProps) {
  const { tableData } = props
  const data = useMemo(() => tableData, [])
  const columns = useMemo(() => resultsColumns, []) as Column<any>[]

  return <DataTable tableName={"Saved Records"} tableColumns={columns} tableData={data} />
}
