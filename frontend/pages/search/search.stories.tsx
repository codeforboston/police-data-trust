import React from "react"
import { Meta } from "@storybook/react"
import Dashboard from "./"
import { AuthProvider } from "../../helpers"

export default {
  title: "Pages/Dashboard",
  component: Dashboard,
  decorators: [
    (Story) => (
      <AuthProvider>
        <Story />
      </AuthProvider>
    )
  ]
} as Meta<typeof Dashboard>

export const Default = <Dashboard />