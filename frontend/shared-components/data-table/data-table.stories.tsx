import { ComponentMeta, ComponentStory } from "@storybook/react"
import React from "react"
import { mockIncident } from "../../models/mock-data"
import { resultsColumns, tableColumns } from "../../models/mock-data/mock-table-data"
import { DataTable } from "./data-table"
export default {
  title: "Shared Components/Data Table",
  component: DataTable
} as ComponentMeta<typeof DataTable>

const Template: ComponentStory<typeof DataTable> = (args) => <DataTable {...args} />

export const Default = Template.bind({})

Default.args = {
  tableTitle: "Data Table",
  tableColumns: resultsColumns,
  tableData: mockIncident
}
