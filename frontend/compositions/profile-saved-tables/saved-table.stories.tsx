import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import SavedTable from "./saved-table"
import { faAngleRight, faCaretRight } from "@fortawesome/free-solid-svg-icons"

import { resultsColumns, searchesColumns } from "../../models/saved-table"
import { mockSavedSearches, mockSavedResults } from "../../models/mock-data"

export default {
  title: "Compositions/Saved Table",
  component: SavedTable
} as ComponentMeta<typeof SavedTable>

const Template: ComponentStory<typeof SavedTable> = (args) => <SavedTable {...args} />

export const SavedResultsTable = Template.bind({})
SavedResultsTable.args = {
  itemTitle: "Results",
  tableColumns: resultsColumns,
  tableData: mockSavedResults,
  rowIdName: "recordId",
  expandIcon: faAngleRight
}

export const SavedSearchTable = Template.bind({})
SavedSearchTable.args = {
  itemTitle: "Searches",
  tableColumns: searchesColumns,
  tableData: mockSavedSearches,
  rowIdName: "results",
  expandIcon: faCaretRight
}
