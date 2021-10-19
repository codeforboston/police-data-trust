import React from "react"
import { DataTable } from "../../shared-components/data-table/data-table"
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout, PrimaryInput } from "../../shared-components"
import { requireAuth } from "../../helpers"
import { AppRoutes, CallToActionTypes, PrimaryInputNames } from "../../models"
import { FormProvider, useForm } from "react-hook-form"
const { INCIDENT_TYPE, DATE_TIME, OFFICER_NAME, LOCATION, BADGE_NUMBER } = PrimaryInputNames

const SearchPanel = () => {
  const [incidentMode, setIncidentMode] = React.useState(false)
  const form = useForm()
  const toIncident = () => {
    setIncidentMode(true)
  }

  const toOfficer = () => {
    setIncidentMode(false)
  }

  async function onSubmit(formValues: any) {}
  return (
    <div style={{ border: "2px solid black" }}>
      <FormProvider {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          SearchPanel
          <div>
            <button
              onClick={toIncident}
              className={`${incidentMode ? "primaryButton" : "secondaryButton"}`}>
              Incident
            </button>
            <button
              onClick={toOfficer}
              className={`${incidentMode ? "secondaryButton" : "primaryButton"}`}>
              Officer
            </button>
          </div>
          {incidentMode ? (
            <div>
              <div>
                <PrimaryInput inputName={LOCATION} />
              </div>
              <div>
                <PrimaryInput inputName={INCIDENT_TYPE} />
              </div>
              <div>
                <PrimaryInput inputName={DATE_TIME} />
              </div>
            </div>
          ) : (
            <div>
              <div>
                <PrimaryInput inputName={OFFICER_NAME} />
              </div>
              <div>
                <PrimaryInput inputName={LOCATION} />
              </div>
              <div>
                <PrimaryInput inputName={BADGE_NUMBER} />
              </div>
            </div>
          )}
        </form>
      </FormProvider>
    </div>
  )
}

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <SearchPanel />
      <Map />
      <DataTable />
    </Layout>
  )
})
