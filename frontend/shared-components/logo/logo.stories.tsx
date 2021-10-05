import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { Logo } from ".."
import { LogoSizes } from "../../models"

export default {
  title: "Shared Components/Logo",
  component: Logo
} as ComponentMeta<typeof Logo>

const Template: ComponentStory<typeof Logo> = (args) => <Logo {...args} />

export const Large = Template.bind({})
Large.args = { size: LogoSizes.LARGE }

export const Medium = Template.bind({})
Medium.args = { size: LogoSizes.MEDIUM }

export const Small = Template.bind({})
Small.args = { size: LogoSizes.SMALL }

export const Tiny = Template.bind({})
Tiny.args = { size: LogoSizes.XSMALL }
