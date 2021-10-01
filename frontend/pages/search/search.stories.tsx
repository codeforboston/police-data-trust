import React from "react"
import { ComponentMeta } from "@storybook/react"
import Dashboard from "."
import { FormProvider, useForm } from "react-hook-form"
import { AuthProvider } from "../../helpers"

export default {
  title: "Pages/Dashboard",
  component: Dashboard,
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
} as ComponentMeta<typeof Dashboard>

export const Default = <Dashboard />