import React from "react"
import { Story, Meta } from "@storybook/react"
import { DashboardHeader } from ".."

export default {
  title: "Compositions/Header",
  component: DashboardHeader
} as Meta<typeof DashboardHeader>

const Template: Story<typeof DashboardHeader> = (args: any) => <DashboardHeader {...args} />

export const Default = Template.bind({})
Default.parameters = {
  controls: { hideNoControlsWarning: true }
}
