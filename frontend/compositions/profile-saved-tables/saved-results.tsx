import SavedTable from "./saved-table"
import { faAngleRight } from "@fortawesome/free-solid-svg-icons"

import { SavedResultsType, resultsColumns } from "../../models/saved-table"
import { mockSavedResults } from "../../models/mock-data"


interface SavedResultsProps {
  data?: Array<SavedResultsType>
}

export default function SavedResults({ data = mockSavedResults }: SavedResultsProps) {
  return SavedTable({
    itemTitle: "Results",
    tableColumns: resultsColumns,
    tableData: data,
    rowIdName: "id",
    expandIcon: faAngleRight
  })
}
