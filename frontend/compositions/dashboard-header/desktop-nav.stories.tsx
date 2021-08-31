import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react';
import DesktopNav from './desktop-nav'

export default {
  title: 'Compositions/Desktop Nav',
  component: DesktopNav
} as ComponentMeta<typeof DesktopNav>

const Template: ComponentStory<typeof DesktopNav> = (args) => <DesktopNav {...args} />

export const LoggedIn = Template.bind({});
LoggedIn.args = {
  user: {},
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {};
