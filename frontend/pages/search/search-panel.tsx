import React from "react"
import { DataTable } from "../../shared-components/data-table/data-table"
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout, PrimaryButton, PrimaryInput } from "../../shared-components"
import { requireAuth } from "../../helpers"
import { AppRoutes, CallToActionTypes, PrimaryInputNames } from "../../models"
import { FormProvider, useForm } from "react-hook-form"
import styles from "./search.module.css"
const { KEY_WORDS, DATE, OFFICER_NAME, LOCATION, BADGE_NUMBER } = PrimaryInputNames

const { searchToggle, selectedSearch, searchChoices, searchPanelContainer, searchForm } = styles

export const SearchPanel = () => {
  const form = useForm()
  const [incidentSearch, setIncidentSearch] = React.useState(true)
  const [loading, setLoading] = React.useState(false)
  const toIncident = () => {
    setIncidentSearch(true)
  }

  const toOfficer = () => {
    setIncidentSearch(false)
  }

  async function onSubmit(formValues: any) {
    setLoading(true)
    try {
      // TODO
    } catch (e) {
      console.error("Unexpected login error", e)
    }
    console.log(formValues)
    setLoading(false)
  }
  return (
    <div className={searchPanelContainer}>
      <FormProvider {...form}>
        <form className={searchForm} onSubmit={form.handleSubmit(onSubmit)}>
          <div className={searchToggle}>
            <div>I am searching for...</div>
            <div className={searchChoices}>
              <div onClick={toIncident} className={`${incidentSearch ? selectedSearch : ""}`}>
                Incident(s)
              </div>
              <div onClick={toOfficer} className={`${incidentSearch ? "" : selectedSearch}`}>
                Officer(s)
              </div>
            </div>
          </div>
          {incidentSearch ? (
            <div>
              <div>
                <PrimaryInput inputName={LOCATION} />
              </div>
              <div>
                <PrimaryInput inputName={KEY_WORDS} />
              </div>
              <div>
                <PrimaryInput inputName={DATE} />
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
          <PrimaryButton loading={loading} type="submit">
            Search
          </PrimaryButton>
        </form>
      </FormProvider>
    </div>
  )
}
