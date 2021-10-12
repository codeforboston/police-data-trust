import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import ViewerRegistration from "../pages/register"

export default {
  title: "Pages/Registration",
  component: ViewerRegistration
} as ComponentMeta<typeof ViewerRegistration>

const Template: ComponentStory<typeof ViewerRegistration> = (args) => (
  <ViewerRegistration {...args} />
)

export const Register = Template.bind({})
Register.parameters = {
  controls: { hideNoControlsWarning: true },
  user: false
}
