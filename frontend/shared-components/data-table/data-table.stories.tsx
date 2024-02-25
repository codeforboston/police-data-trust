import { ComponentMeta, ComponentStory } from "@storybook/react"
import React from "react"
import { EXISTING_TEST_INCIDENTS } from "../../helpers/api/mocks/data"
import { DataTable } from "./data-table"
import { savedResultsColumns } from "../../compositions/profile-saved-tables/saved-results"
import { resultsColumns } from "../../compositions/search-results/search-results"
import { searchesColumns } from "../../compositions/profile-saved-tables/saved-searches"

export default {
  title: "Shared Components/Data Table",
  component: DataTable
} as ComponentMeta<typeof DataTable>

const Template: ComponentStory<typeof DataTable> = (args) => <DataTable {...args} />

export const SearchResults = Template.bind({})

SearchResults.args = {
  tableName: "Search Results",
  columns: resultsColumns,
  data: EXISTING_TEST_INCIDENTS
}

export const SavedResults = Template.bind({})

SavedResults.args = {
  tableName: "Saved Results",
  columns: savedResultsColumns,
  data: EXISTING_TEST_INCIDENTS
}
