import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { SuccessMessage } from ".."

export default {
  title: "Shared Components/Success Message",
  component: SuccessMessage
} as ComponentMeta<typeof SuccessMessage>

const Template: ComponentStory<typeof SuccessMessage> = (args) => <SuccessMessage {...args} />

export const Default = Template.bind({})
Default.args = {
  message: "This is a success message"
}
