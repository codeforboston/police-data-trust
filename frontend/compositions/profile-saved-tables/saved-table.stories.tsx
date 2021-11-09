import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { faAngleRight, faCaretRight } from "@fortawesome/free-solid-svg-icons"

import { resultsColumns, searchesColumns } from "../../models/saved-table"
import { mockSavedSearches, mockSavedResults } from "../../models/mock-data"
import { DataTable } from "../../shared-components/data-table/data-table"
import { mockIncident } from "../../models/mock-data"

export default {
  title: "Compositions/Saved Table",
  component: DataTable
} as ComponentMeta<typeof DataTable>

const Template: ComponentStory<typeof DataTable> = (args) => <DataTable {...args} />

export const SavedResultsTable = Template.bind({})
SavedResultsTable.args = {
  tableTitle: "Results",
  tableColumns: resultsColumns,
  tableData: mockIncident,
  // rowIdName: "recordId",
  // expandIcon: faAngleRight
}

export const SavedSearchTable = Template.bind({})
SavedSearchTable.args = {
  itemTitle: "Searches",
  tableColumns: searchesColumns,
  tableData: mockSavedSearches,
  // rowIdName: "results",
  // expandIcon: faCaretRight
}
