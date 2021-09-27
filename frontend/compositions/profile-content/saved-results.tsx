import SavedTable from "./saved-table"
import { faAngleRight } from "@fortawesome/free-solid-svg-icons"

import { resultsColumns } from "../../models/search-meta"
import { savedResultsData } from "../../models/mock-data"

// TODO: retrieve user saved results from API

export default function SavedResults() {
  return SavedTable({
    itemTitle: "Results",
    tableColumns: resultsColumns,
    tableData: savedResultsData,
    rowIdName: "recordId",
    expandIcon: faAngleRight
  })
}
