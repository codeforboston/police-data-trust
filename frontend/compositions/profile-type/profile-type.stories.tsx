import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import ProfileType from "."
import users from "../../models/mock-data/users.json"

export default {
  title: "Compositions/Profile Type",
  component: ProfileType
} as ComponentMeta<typeof ProfileType>

const Template: ComponentStory<typeof ProfileType> = (args) => <ProfileType {...args} />

export const PublicProfile = Template.bind({})
PublicProfile.args = {
  userData: users[0]
}

export const PassportProfile = Template.bind({})
PassportProfile.args = {
  userData: users[1]
}
