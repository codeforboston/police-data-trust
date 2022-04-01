import { ComponentStory, ComponentMeta } from "@storybook/react"
import IncidentData from "."
import sampleIncident, { Incident } from '../../../../helpers/incident'

export default {
  title: "Compositions/Incident View Components/IncidentData"
} as ComponentMeta<typeof IncidentData>

const Template: ComponentStory<typeof IncidentData> = (args : Incident) => (
  <IncidentData {...args} />
)

export const Blank = Template.bind({})
Blank.args = sampleIncident()
