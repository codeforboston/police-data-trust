import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { PrimaryInput } from ".."
import { PrimaryInputNames } from "../../models"

export default {
  title: "Shared Components/Primary Input",
  component: PrimaryInput
} as ComponentMeta<typeof PrimaryInput>

const Template: ComponentStory<typeof PrimaryInput> = (args) => <PrimaryInput {...args} />

export const FirstNameInput = Template.bind({})
FirstNameInput.args = {
  inputName: PrimaryInputNames.FIRST_NAME
}

export const LastNameInput = Template.bind({})
LastNameInput.args = {
  inputName: PrimaryInputNames.LAST_NAME
}

export const EmailAddressInput = Template.bind({})
EmailAddressInput.args = {
  inputName: PrimaryInputNames.EMAIL_ADDRESS
}

export const PhoneNumberInput = Template.bind({})
PhoneNumberInput.args = {
  inputName: PrimaryInputNames.PHONE_NUMBER
}

export const CreatePasswordInput = Template.bind({})
CreatePasswordInput.args = {
  inputName: PrimaryInputNames.CREATE_PASSWORD
}

export const ConfirmPasswordInput = Template.bind({})
ConfirmPasswordInput.args = {
  inputName: PrimaryInputNames.CONFIRM_PASSWORD
}

export const StreetAddressInput = Template.bind({})
StreetAddressInput.args = {
  inputName: PrimaryInputNames.STREET_ADDRESS
}

export const ZipCodeInput = Template.bind({})
ZipCodeInput.args = {
  inputName: PrimaryInputNames.ZIP_CODE
}
