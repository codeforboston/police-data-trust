import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { SuccessPage } from ".."

export default {
  title: "Shared Components/Success Page",
  component: SuccessPage
} as ComponentMeta<typeof SuccessPage>

const Template: ComponentStory<typeof SuccessPage> = (args) => <SuccessPage {...args} />

export const Default = Template.bind({})