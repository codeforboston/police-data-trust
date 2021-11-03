import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import ResultsAlert from "./results-alert"
import { SearchResultsTypes } from "../../models/results-alert"

export default {
  title: "Shared Components/Results Alert",
  component: ResultsAlert
} as ComponentMeta<typeof ResultsAlert>

const Template: ComponentStory<typeof ResultsAlert> = (args: any) => <ResultsAlert {...args} />

export const NoResults = Template.bind({})
NoResults.args = {
  type: SearchResultsTypes.NORESULTS,
  returnHandler: () => {}
}
export const NoParams = Template.bind({})
NoParams.args = {
  type: SearchResultsTypes.NOSEARCHPARAMS,
  returnHandler: () => {}
}
