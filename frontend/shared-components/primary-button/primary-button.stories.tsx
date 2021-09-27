import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { PrimaryButton } from ".."

export default {
  title: "Shared Components/Primary Button",
  component: PrimaryButton
} as ComponentMeta<typeof PrimaryButton>

const Template: ComponentStory<typeof PrimaryButton> = (args) => <PrimaryButton {...args} />

export const Button = Template.bind({})
Button.args = {
  loading: false,
  children: "Button"
}
