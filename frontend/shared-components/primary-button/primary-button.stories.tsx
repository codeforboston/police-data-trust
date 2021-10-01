import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { PrimaryButton } from ".."

export default {
  title: "Shared Components/Primary Button",
  component: PrimaryButton
} as ComponentMeta<typeof PrimaryButton>

const Template: ComponentStory<typeof PrimaryButton> = (args) => <PrimaryButton {...args} />

export const Default = Template.bind({})
Default.args = {
  loading: false,
  children: "Button"
}

export const Loading = Template.bind({})
Loading.args = {
  loading: true
}
