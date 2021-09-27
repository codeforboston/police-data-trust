import React from 'react'
import { ComponentStory, ComponentMeta } from '@storybook/react'
import { DataTable } from './data-table'

export default {
  title: 'Shared Components/Data Table',
  component: DataTable
} as ComponentMeta<typeof DataTable>

const Template: ComponentStory<typeof DataTable> = (args) => <DataTable {...args} />

export const BasicTable = Template.bind({})
BasicTable.args = {

}