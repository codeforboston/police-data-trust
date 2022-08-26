import { ComponentStory, ComponentMeta } from "@storybook/react"
import IncidentViewHeader from "."

export default {
  title: "Compositions/Incident View Components/IncidentHeader"
} as ComponentMeta<typeof IncidentViewHeader>

const Template: ComponentStory<typeof IncidentViewHeader> = (args) => (
  <IncidentViewHeader {...args} />
)

export const Blank = Template.bind({})
