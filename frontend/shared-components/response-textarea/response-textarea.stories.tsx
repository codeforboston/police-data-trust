import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { ResponseTextArea } from ".."
import { Providers } from "../../helpers"

export default {
  title: "Shared Components/Response Text Area",
  component: ResponseTextArea
} as ComponentMeta<typeof ResponseTextArea>

const Template: ComponentStory<typeof ResponseTextArea> = (args) => <ResponseTextArea {...args} />

export const Default = Template.bind({})
