import React, { useMemo } from "react"
import { Column } from "react-table"
import { SavedSearchType, searchesColumns } from "../../models/saved-table"
import { DataTable } from "../../shared-components/data-table/data-table"

// TODO: retrieve user saved searches from API

interface SavedSearchProps {
  tableData?: SavedSearchType[]
}

export default function SavedSearches(props: SavedSearchProps) {
  const { tableData } = props
  const data = useMemo(() => tableData, [])
  const columns = useMemo(() => searchesColumns, []) as Column<any>[]
  return <DataTable tableName={"Saved Searches"} tableColumns={columns} tableData={data} />
}
