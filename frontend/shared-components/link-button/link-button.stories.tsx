import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import {LinkButton} from ".."

export default {
    title: "Shared Components/Link Button",
    component: LinkButton
  } as ComponentMeta<typeof LinkButton>

const Template: ComponentStory<typeof LinkButton> = (args) => <LinkButton {...args} />

export const Default = Template.bind({})
Default.args = {
  loading: false,
  children: "Button"
}