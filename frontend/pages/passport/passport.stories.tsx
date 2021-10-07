import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import Passport from "."

export default {
  title: "Pages/Passport Registration",
  component: Passport
} as ComponentMeta<typeof Passport>

const Template: ComponentStory<typeof Passport> = (args) => <Passport {...args} />

export const Register = Template.bind({})
Register.parameters = {
  controls: { hideNoControlsWarning: true }
}
