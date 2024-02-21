import React from "react"
import { StoryFn, Meta } from "@storybook/react"
import { DashboardHeader } from ".."

export default {
  title: "Compositions/Header",
  component: DashboardHeader
} as Meta<typeof DashboardHeader>

const Template: StoryFn<typeof DashboardHeader> = (args: any) => <DashboardHeader {...args} />

export const Default = Template.bind({})
Default.parameters = {
  controls: { hideNoControlsWarning: true }
}
