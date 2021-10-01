import React from "react"
import { Meta } from "@storybook/react"
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
  ],
} as Meta<typeof Passport>

export const PassportRegistration = <Passport />