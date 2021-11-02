import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import Profile from "../pages/profile"

export default {
  title: "Pages/ProfilePage",
  component: Profile
} as ComponentMeta<typeof Profile>

const Template: ComponentStory<typeof Profile> = (args) => <Profile {...args} />
export const ProfilePage = Template.bind({})
ProfilePage.parameters = {
  controls: { hideNoControlsWarning: true }
}
