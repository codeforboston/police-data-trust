import { ComponentMeta, ComponentStory } from "@storybook/react"
import React from "react"
import { OfficerIncidentDataTable } from "./officer-incident-data-table"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"
import { incidentResultsColumns } from "../../models/officer"

export default {
  title: "Shared Components/Officer Incident Data Table",
  component: OfficerIncidentDataTable
} as ComponentMeta<typeof OfficerIncidentDataTable>

const Template: ComponentStory<typeof OfficerIncidentDataTable> = (args) => (
  <OfficerIncidentDataTable {...args} />
)

export const OfficerIncidentResults = Template.bind({})

OfficerIncidentResults.args = {
  columns: incidentResultsColumns,
  data: getOfficerFromMockData(0).incidents
}