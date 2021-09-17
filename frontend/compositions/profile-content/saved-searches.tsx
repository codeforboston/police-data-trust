import SavedTable from "./saved-table"
import { faCaretRight } from "@fortawesome/free-solid-svg-icons"

import { searchesColumns } from "../../models/search-meta"
import { savedSearchData } from "../../models/mock-data"

// TODO: retrieve user saved searches from API

export default function SavedSearches() {
  return SavedTable({
    itemTitle: 'Searches',
    tableColumns: searchesColumns,
    tableData: savedSearchData,
    rowIdName: 'results',
    expandIcon: faCaretRight
  })
}
