import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { FormProvider, useForm } from "react-hook-form"
import { AuthProvider } from "../../helpers"
import Passport from "."

export default {
  title: "Pages/Passport Registration",
  component: Passport,
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
} as ComponentMeta<typeof Passport>

const Template: ComponentStory<typeof Passport> = (args) => <Passport {...args} />
export const PassportRegistration = Template.bind({})
PassportRegistration.parameters = {
  controls: { hideNoControlsWarning: true }
}
