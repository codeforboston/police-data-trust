import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { EnrollmentCallToAction } from ".."
import { CallToActionTypes } from "../../models"

export default {
  title: "Compositions/Enrollment Call-to-Action",
  component: EnrollmentCallToAction
} as ComponentMeta<typeof EnrollmentCallToAction>

const Template: ComponentStory<typeof EnrollmentCallToAction> = (args) => (
  <EnrollmentCallToAction {...args} />
)

export const RegisterCTA = Template.bind({})
RegisterCTA.args = {
  callToActionType: CallToActionTypes.REGISTER
}

export const DashboardCTA = Template.bind({})
DashboardCTA.args = {
  callToActionType: CallToActionTypes.DASHBOARD
}

export const LoginCTA = Template.bind({})
LoginCTA.args = {
  callToActionType: CallToActionTypes.LOGIN
}
