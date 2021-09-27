import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react'
import { ResponseTextArea } from '..'

export default {
  title: 'Shared Components/Response Text Area',
  component: ResponseTextArea
} as ComponentMeta<typeof ResponseTextArea>

const Template: ComponentStory<typeof ResponseTextArea> = (args) => <ResponseTextArea {...args} />

export const BasicTextArea = Template.bind({
  isSubmitted: false
})