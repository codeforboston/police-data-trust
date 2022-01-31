import { ComponentMeta, ComponentStory } from "@storybook/react"
import OptionalOfficerData from "./"
import officers from "../../../models/mock-data/officer.json"

export default {
  title: "Compositions/Officer View Components/OptionalOfficerData"
} as ComponentMeta<typeof OptionalOfficerData>

const Template: ComponentStory<typeof OptionalOfficerData> = (args) => (
  <OptionalOfficerData {...args} />
)

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = officers[0]
