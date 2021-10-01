import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { PassportApplicationResponse, RegistrationResponse } from ".."

export default {
  title: "Compositions/Enrollment Response",
  component: PassportApplicationResponse
} as ComponentMeta<typeof PassportApplicationResponse>

const PassportTemplate: ComponentStory<typeof PassportApplicationResponse> = (args) => (
  <PassportApplicationResponse {...args} />
)

const RegisterTemplate: ComponentStory<typeof RegistrationResponse> = (args) => (
  <RegistrationResponse {...args} />
)

export const PassportSuccess = PassportTemplate.bind({})
PassportSuccess.args = {
  success: true
}

export const PassportFail = PassportTemplate.bind({})
PassportFail.args = {
  success: false
}

export const RegistrationSuccess = RegisterTemplate.bind({})
RegistrationSuccess.args = {
  success: true
}

export const RegistrationFail = RegisterTemplate.bind({})
RegistrationFail.args = {
  success: false
}
