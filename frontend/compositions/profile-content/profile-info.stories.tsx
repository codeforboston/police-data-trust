import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { ProfileInfo } from "."
import { FormProvider, useForm } from "react-hook-form"
import users from "../../models/mock-data/users.json"

export default {
  title: "Compositions/Profile Info",
  component: ProfileInfo,
  decorators: [
    (Story) => {
      const methods = useForm()
      return (
        <FormProvider {...methods}>
          <Story />
        </FormProvider>
      )
    }
  ]
} as ComponentMeta<typeof ProfileInfo>

const Template: ComponentStory<typeof ProfileInfo> = (args) => <ProfileInfo {...args} />

export const Default = Template.bind({})
Default.args = {
  userData: users[0]
}
