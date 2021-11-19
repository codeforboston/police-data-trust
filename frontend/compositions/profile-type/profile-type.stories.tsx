import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import ProfileType from "."

export default {
  title: "Compositions/Profile Type",
  component: ProfileType
} as ComponentMeta<typeof ProfileType>

const Template: ComponentStory<typeof ProfileType> = (args) => <ProfileType {...args} />

export const Default = Template.bind({})
