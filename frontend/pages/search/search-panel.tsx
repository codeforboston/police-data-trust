import React from "react"
import { FormProvider, useForm } from "react-hook-form"
import { useAuth, useSearch } from "../../helpers"
import { PrimaryInputNames } from "../../models"
import { FormLevelError, PrimaryButton, PrimaryInput } from "../../shared-components"
import styles from "./search.module.css"
const { KEY_WORDS, DATE_START, DATE_END, OFFICER_NAME, LOCATION, BADGE_NUMBER } = PrimaryInputNames

const { searchToggle, selectedSearch, searchChoices, searchPanelContainer, searchForm } = styles

export const SearchPanel = () => {
  const form = useForm()
  const { searchIncidents } = useSearch()
  const { accessToken } = useAuth()
  const [submitError, setSubmitError] = React.useState(null)

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
      await searchIncidents({
        accessToken,
        location: formValues[LOCATION],
        startTime: formValues[DATE_START],
        endTime: formValues[DATE_END],
        description: formValues[KEY_WORDS]
      })
    } catch (e) {
      console.error("Unexpected search error", e)
      setSubmitError("Something went wrong. Please try again.")
    }
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
                <PrimaryInput inputName={DATE_START} />
              </div>
              <div>
                <PrimaryInput inputName={DATE_END} />
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
          {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}

          <PrimaryButton loading={loading} type="submit">
            Search
          </PrimaryButton>
        </form>
      </FormProvider>
    </div>
  )
}
