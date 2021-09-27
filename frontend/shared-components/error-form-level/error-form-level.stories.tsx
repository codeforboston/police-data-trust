import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { FormLevelError } from ".."

export default {
  title: "Shared Components/Form Error",
  component: FormLevelError
} as ComponentMeta<typeof FormLevelError>

const Template: ComponentStory<typeof FormLevelError> = (args) => <FormLevelError {...args} />

export const BasicError = Template.bind({})
BasicError.args = {
  errorId: 1,
  errorMessage: "An error has occurred"
}
