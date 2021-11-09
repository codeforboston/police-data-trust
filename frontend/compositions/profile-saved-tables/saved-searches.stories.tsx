import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import SavedSearches from "./saved-searches"
import { mockSavedSearches } from "../../models/mock-data"

export default {
  title: "Compositions/Saved Searches",
  component: SavedSearches
} as ComponentMeta<typeof SavedSearches>

const Template: ComponentStory<typeof SavedSearches> = (args) => <SavedSearches {...args} />

export const Default = Template.bind({})

Default.args = {
  tableData: mockSavedSearches
}
