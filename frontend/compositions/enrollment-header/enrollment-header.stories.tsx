import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { EnrollmentHeader } from ".."
import { TooltipTypes } from "../../models"

export default {
  title: "Compositions/Enrollment Header",
  component: EnrollmentHeader
} as ComponentMeta<typeof EnrollmentHeader>

const Template: ComponentStory<typeof EnrollmentHeader> = (args) => <EnrollmentHeader {...args} />

export const ViewerEnrollmentHeader = Template.bind({})
ViewerEnrollmentHeader.args = {
  headerText: "Viewer Registration",
  tooltip: TooltipTypes.VIEWER
}

export const IncidentEnrollmentHeader = Template.bind({})
IncidentEnrollmentHeader.args = {
  headerText: "Incident Header",
  tooltip: TooltipTypes.INCIDENTS
}
