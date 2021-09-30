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

export const DonateButton = Template.bind({})
DonateButton.args = {
  loading: false,
  children: "DONATE",
  style: {
    fontWeight: "bold"
  }
}

export const SecondaryButton = Template.bind({})
SecondaryButton.args = {
  loading: false,
  children: "Secondary",
  style: {
    border: "thin solid #303463",
    backgroundColor: "white",
    color: "#303463"
  }
}

export const Loading = Template.bind({})
Loading.args = {
  loading: true
}

