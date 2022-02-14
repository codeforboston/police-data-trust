import { ComponentStory, ComponentMeta } from "@storybook/react"
import OfficerHeader from "."
import { getOfficerFromMockData } from "../../../helpers/mock-to-officer-type"

export default {
  title: "Compositions/Officer View Components/OfficerHeader"
} as ComponentMeta<typeof OfficerHeader>

const Template: ComponentStory<typeof OfficerHeader> = (args) => <OfficerHeader {...args} />

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = getOfficerFromMockData(0)
