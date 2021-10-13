import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { InfoTooltip } from ".."
import { TooltipTypes } from "../../models"

export default {
  title: "Shared Components/Info Tooltip",
  component: InfoTooltip,
  decorators: [
    (Story) => (
      <div style={{ margin: "8rem 0 0 4rem" }}>
        <Story />
      </div>
    )
  ]
} as ComponentMeta<typeof InfoTooltip>

const Template: ComponentStory<typeof InfoTooltip> = (args) => <InfoTooltip {...args} />

export const ViewerTooltip = Template.bind({})
ViewerTooltip.args = {
  type: TooltipTypes.VIEWER
}

export const IncidentTooltip = Template.bind({})
IncidentTooltip.args = {
  type: TooltipTypes.INCIDENTS
}
