import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { FormLevelError } from ".."

export default {
  title: "Shared Components/Form Error",
  component: FormLevelError,
  argTypes: {
    errorId: {
      control: { type: "number" }
    },
    errorMessage: {
      control: { type: "text" }
    }
  }
} as ComponentMeta<typeof FormLevelError>

const Template: ComponentStory<typeof FormLevelError> = (args) => <FormLevelError {...args} />

export const Default = Template.bind({})
Default.args = {
  errorId: 1,
  errorMessage: "An error has occurred"
}

export const AnotherError = Template.bind({})
AnotherError.args = {
  errorId: 2,
  errorMessage: "A different error has occurred"
}
