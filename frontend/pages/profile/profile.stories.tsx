import React from "react"
import { Meta } from "@storybook/react"
import Profile from "./"
import { AuthProvider } from "../../helpers"

export default {
  title: "Pages/Profile",
  component: Profile,
  decorators: [
    (Story) => (
      <AuthProvider>
        <Story />
      </AuthProvider>
    )
  ]
} as Meta<typeof Profile>

export const ProfilePage = <Profile />