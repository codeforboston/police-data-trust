import React from 'react'
import { Story, Meta } from '@storybook/react'
import { RegistrationResponse } from '..'

export default {
  title: 'Compositions/Registration Response',
  component: RegistrationResponse
} as Meta<typeof RegistrationResponse>

const Template: Story<typeof RegistrationResponse> = (args) => <RegistrationResponse {...args} />

export const RegistrationSuccess = Template.bind({})
RegistrationSuccess.args = {
  success: true
}

export const RegistrationFailure = Template.bind({})
RegistrationFailure.args = {
  success: false
}
