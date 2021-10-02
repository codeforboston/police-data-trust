import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { Providers } from "../../helpers"
import UserLogin from "."

export default {
  title: "Pages/Login",
  component: UserLogin,
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ]
} as ComponentMeta<typeof UserLogin>

const Template: ComponentStory<typeof UserLogin> = (args) => <UserLogin {...args} />

export const Login = Template.bind({})
Login.parameters = {
  controls: { hideNoControlsWarning: true }
}
