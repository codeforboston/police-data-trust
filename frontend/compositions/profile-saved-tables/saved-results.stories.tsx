import { ComponentMeta, ComponentStory } from "@storybook/react"
import React from "react"
import { mockSavedResults } from "../../models/mock-data"
import SavedResults from "./saved-results"

export default {
  title: "Compositions/Saved Results",
  component: SavedResults
} as ComponentMeta<typeof SavedResults>

const Template: ComponentStory<typeof SavedResults> = (args) => <SavedResults {...args} />

export const Default = Template.bind({})

Default.args = {
  tableData: mockSavedResults
}
