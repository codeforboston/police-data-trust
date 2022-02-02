import { ComponentMeta, ComponentStory } from "@storybook/react"
import OfficerAffiliations from "."
import { getOfficerFromMockData } from "../../../helpers/mock-to-officer-type"

export default {
  title: "Compositions/Officer View Components/OfficerAffiliations"
} as ComponentMeta<typeof OfficerAffiliations>

const Template: ComponentStory<typeof OfficerAffiliations> = (args) => (
  <OfficerAffiliations {...args} />
)

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = getOfficerFromMockData(0)
