import { ComponentMeta, ComponentStory } from "@storybook/react"
import OfficerWorkHistory from "./"
import { getOfficerFromMockData } from "../../../helpers/mock-to-officer-type"

export default {
  title: "Compositions/Officer View Components/OfficerWorkHistory"
} as ComponentMeta<typeof OfficerWorkHistory>

const Template: ComponentStory<typeof OfficerWorkHistory> = (args) => (
  <OfficerWorkHistory {...args} />
)

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = getOfficerFromMockData(0)
