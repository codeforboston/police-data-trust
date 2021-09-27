import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { PassportApplicationResponse } from ".."

export default {
  title: "Compositions/Passport Response",
  component: PassportApplicationResponse
} as ComponentMeta<typeof PassportApplicationResponse>

const Template: ComponentStory<typeof PassportApplicationResponse> = (args) => (
  <PassportApplicationResponse {...args} />
)

export const PassportSuccess = Template.bind({})
PassportSuccess.args = {
  success: true
}

export const PassportFailure = Template.bind({})
PassportFailure.args = {
  success: false
}
