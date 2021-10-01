import React from "react"
import { Meta } from "@storybook/react"
import ViewerRegistration from "./"
import { FormProvider, useForm } from "react-hook-form"
import { AuthProvider } from "../../helpers"


export default {
  title: "Pages/Viewer Registration",
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
  ],
} as Meta<typeof ViewerRegistration>

export const Registration = <ViewerRegistration />
