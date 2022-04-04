import { ComponentMeta, ComponentStory } from "@storybook/react"
import IncidentView from "../pages/incident-view"

export default {
  title: "Pages/IncidentView",
  component: IncidentView
} as ComponentMeta<typeof IncidentView>

const Template: ComponentStory<typeof IncidentView> = (args) => <IncidentView {...args} />

export const Login = Template.bind({})
