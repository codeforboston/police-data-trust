import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { ResponseTextArea } from ".."
import { FormProvider, useForm } from "react-hook-form"

export default {
  title: "Shared Components/Response Text Area",
  component: ResponseTextArea,
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
} as ComponentMeta<typeof ResponseTextArea>

const Template: ComponentStory<typeof ResponseTextArea> = (args) => <ResponseTextArea {...args} />

export const Default = Template.bind({})