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

export const PassportResponse = PassportTemplate.bind({})
PassportResponse.args = {
  success: true
}

export const RegistraterResponse = RegisterTemplate.bind({})
RegistraterResponse.args = {
  success: true
}
