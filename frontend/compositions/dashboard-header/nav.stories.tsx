import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import Nav from "./nav"

export default {
  title: "Compositions/Desktop Nav",
  component: Nav
} as ComponentMeta<typeof Nav>

const Template: ComponentStory<typeof Nav> = (args) => <Nav {...args} />

export const DesktopNav = Template.bind({})
DesktopNav.args = {}
