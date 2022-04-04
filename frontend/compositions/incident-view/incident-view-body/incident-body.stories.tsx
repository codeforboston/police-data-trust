import { ComponentStory, ComponentMeta } from "@storybook/react"
import IncidentBody from "."
import sampleIncident, { Incident } from "../../../helpers/incident"

export default {
  title: "Compositions/Incident View Components/Incident Body"
} as ComponentMeta<typeof IncidentBody>

const Template: ComponentStory<typeof IncidentBody> = (args: Incident) => <IncidentBody {...args} />

export const Blank = Template.bind({})
Blank.args = sampleIncident()
