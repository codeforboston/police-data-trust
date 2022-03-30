import { ComponentStory, ComponentMeta } from "@storybook/react"
import IncidentViewHeader from "."
import incidents from "../../../models/mock-data/incidents.json"

export default {
  title: "Compositions/Incident View Components/IncidentHeader"
} as ComponentMeta<typeof IncidentViewHeader>

const Template: ComponentStory<typeof IncidentViewHeader> = (args) => (
  <IncidentViewHeader {...args} />
)

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = incidents[0]
