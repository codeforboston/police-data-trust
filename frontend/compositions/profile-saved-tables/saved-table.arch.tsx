import { ComponentMeta, ComponentStory } from "@storybook/react"
import React from "react"
import { mockIncident, mockSavedSearches } from "../../models/mock-data"
import SavedTable from "./saved-table"

export default {
  title: "Compositions/Saved Table",
  component: SavedTable
} as ComponentMeta<typeof SavedTable>

const Template: ComponentStory<typeof SavedTable> = (args) => <SavedTable {...args} />

export const SavedResultsTable = Template.bind({})
SavedResultsTable.args = {
  tableData: mockIncident
}

export const SavedSearchTable = Template.bind({})
SavedSearchTable.args = {
  tableData: mockSavedSearches
}
