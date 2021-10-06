import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import UserLogin from "../pages/login"

export default {
  title: "Pages/Login",
  component: UserLogin
} as ComponentMeta<typeof UserLogin>

const Template: ComponentStory<typeof UserLogin> = (args) => <UserLogin {...args} />

export const Login = Template.bind({})
Login.parameters = {
  controls: { hideNoControlsWarning: true },
  user: false
}
