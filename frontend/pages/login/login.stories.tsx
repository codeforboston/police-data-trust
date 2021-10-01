import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { FormProvider, useForm } from "react-hook-form"
import { AuthProvider } from "../../helpers"
import UserLogin from "."

export default {
  title: "Pages/Login",
  component: UserLogin,
  decorators: [
    (Story) => {
      const methods = useForm()
      return (
        <AuthProvider>
          <FormProvider {...methods}>
            <Story />
          </FormProvider>
        </AuthProvider>
      )
    }
  ]
} as ComponentMeta<typeof UserLogin>

const Template: ComponentStory<typeof UserLogin> = (args) => <UserLogin {...args} />

export const Login = Template.bind({})
Login.parameters = {
  controls: { hideNoControlsWarning: true }
}

