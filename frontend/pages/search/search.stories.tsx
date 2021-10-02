import React from "react"
import { ComponentMeta } from "@storybook/react"
import Dashboard from "."
import { Providers } from "../../helpers"

export default {
  title: "Pages/Dashboard",
  component: Dashboard,
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ]
} as ComponentMeta<typeof Dashboard>

export const Default = <Dashboard />
