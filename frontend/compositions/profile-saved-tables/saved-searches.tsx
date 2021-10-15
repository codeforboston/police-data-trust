import SavedTable from "./saved-table"
import { faCaretRight } from "@fortawesome/free-solid-svg-icons"

import { searchesColumns, SavedSearchType } from "../../models/saved-table"
import { mockSavedSearches } from "../../models/mock-data"

// TODO: retrieve user saved searches from API

interface SavedSearchProps {
  data?: Array<SavedSearchType>
}

export default function SavedSearches({ data = mockSavedSearches }: SavedSearchProps) {
  return SavedTable({
    itemTitle: "Searches",
    tableColumns: searchesColumns,
    tableData: data,
    rowIdName: "results",
    expandIcon: faCaretRight
  })
}
