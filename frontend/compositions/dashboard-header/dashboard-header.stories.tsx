import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react'
import { DashboardHeader } from '..'

export default {
  title: 'Compositions/Dashboard Header',
  component: DashboardHeader
} as ComponentMeta<typeof DashboardHeader>

const Template: ComponentStory<typeof DashboardHeader> = (args) => <DashboardHeader {...args} />

export const LoggedIn = Template.bind({});
LoggedIn.args = {
  user: {},
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {};
