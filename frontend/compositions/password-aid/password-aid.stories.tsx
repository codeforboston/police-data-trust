import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { PasswordAid } from ".."

export default {
  title: "Compositions/Password Aid",
  component: PasswordAid
} as ComponentMeta<typeof PasswordAid>

const Template: ComponentStory<typeof PasswordAid> = (args) => <PasswordAid {...args} />

export const Default = Template.bind({})
Default.args = {}
