import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { DashboardHeader } from ".."
import { Providers } from "../../helpers"

export default {
  title: "Compositions/Header",
  component: DashboardHeader,
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ]
} as ComponentMeta<typeof DashboardHeader>

const Template: ComponentStory<typeof DashboardHeader> = (args) => <DashboardHeader {...args} />

export const Default = Template.bind({})
Default.parameters = {
  controls: { hideNoControlsWarning: true }
}
