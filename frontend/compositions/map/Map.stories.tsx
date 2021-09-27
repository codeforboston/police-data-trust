import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react'
import { Map } from '..'

export default {
  title: 'Compositions/Map',
  component: Map
} as ComponentMeta<typeof Map>

const Template: ComponentStory<typeof Map> = (args) => <Map {...args} />

export const USMap = Template.bind({})
USMap.args = {
  
}