import { ComponentMeta, ComponentStory } from "@storybook/react"
import WorkHistoryInstance from "."
import { getOfficerFromMockData } from "../../../../helpers/mock-to-officer-type"

export default {
  title: "Compositions/Officer View Components/WorkHistoryInstance"
} as ComponentMeta<typeof WorkHistoryInstance>

const Template: ComponentStory<typeof WorkHistoryInstance> = (args) => (
  <WorkHistoryInstance {...args} />
)

export const TimothyBoston = Template.bind({})
TimothyBoston.args = getOfficerFromMockData(0).workHistory[0]

export const TimothySJ = Template.bind({})
TimothySJ.args = getOfficerFromMockData(0).workHistory[1]
