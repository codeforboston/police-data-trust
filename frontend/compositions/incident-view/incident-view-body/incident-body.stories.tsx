import { ComponentStory, ComponentMeta } from "@storybook/react"
import IncidentBody from "."

export default {
  title: "Compositions/Incident View Components/Incident Body"
} as ComponentMeta<typeof IncidentBody>

const Template: ComponentStory<typeof IncidentBody> = (args) => <IncidentBody {...args} />

export const Blank = Template.bind({})
