import { ComponentMeta, ComponentStory } from "@storybook/react"
import IncidentView from "../pages/incident/[id]"

export default {
  title: "Pages/IncidentView",
  component: IncidentView
} as ComponentMeta<typeof IncidentView>

const Template: ComponentStory<typeof IncidentView> = () => <IncidentView />

export const Login = Template.bind({})
