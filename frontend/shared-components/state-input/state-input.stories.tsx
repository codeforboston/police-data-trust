import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { USAStateInput } from ".."

export default {
  title: "Shared Components/State Input",
  component: USAStateInput
} as ComponentMeta<typeof USAStateInput>

const Template: ComponentStory<typeof USAStateInput> = (args) => <USAStateInput {...args} />

export const Default = Template.bind({})
