import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { USAStateInput } from ".."
import { FormProvider, useForm } from "react-hook-form"

export default {
  title: "Shared Components/State Input",
  component: USAStateInput,
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
} as ComponentMeta<typeof USAStateInput>

const Template: ComponentStory<typeof USAStateInput> = (args) => <USAStateInput {...args} />

export const Default = Template.bind({})
