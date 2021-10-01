import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { FormProvider, useForm } from "react-hook-form"
import { AuthProvider } from "../../helpers"
import ViewerRegistration from "."

export default {
  title: "Pages/Registration",
  component: ViewerRegistration,
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
} as ComponentMeta<typeof ViewerRegistration>

const Template: ComponentStory<typeof ViewerRegistration> = (args) => (
  <ViewerRegistration {...args} />
)

export const Register = Template.bind({})
Register.parameters = {
  controls: { hideNoControlsWarning: true }
}
