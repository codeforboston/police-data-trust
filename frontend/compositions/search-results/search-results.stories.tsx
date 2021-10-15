import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import SearchResultsTable from "./"
// import { IncidentTableData } from "../../models"

export default {
  title: "Compositions/Search Results Table",
  component: SearchResultsTable
} as ComponentMeta<typeof SearchResultsTable>

const Template: ComponentStory<typeof SearchResultsTable> = (args) => (
  <SearchResultsTable {...args} />
)

export const Incidents = Template.bind({})
Incidents.args = {
  incidents: require("../../models/mock-data/incidents.json")
}

export const Grammies = Template.bind({})
Grammies.args = {
  incidents: require("../../models/mock-data/grammy.json")
}
