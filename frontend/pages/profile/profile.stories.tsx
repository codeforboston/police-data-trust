import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import Profile from "."
import { AuthProvider } from "../../helpers"
import { FormProvider, useForm } from "react-hook-form"

export default {
  title: "Pages/ProfilePage",
  component: Profile,
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
} as ComponentMeta<typeof Profile>

const Template: ComponentStory<typeof Profile> = (args) => <Profile {...args} />
export const ProfilePage = Template.bind({})
ProfilePage.parameters = {
  controls: { hideNoControlsWarning: true }
}