import React, { FormEvent, useState } from "react"
import styles from "./contributor.module.css"
import { EnrollmentCallToAction, EnrollmentHeader } from "../../compositions"
import { CallToActionTypes, PrimaryInputNames } from "../../models"
import {
  Layout,
  PrimaryButton,
  PrimaryInput,
  ResponseTextArea,
  USAStateInput
} from "../../shared-components"
import { requireAuth, useAuth } from "../../helpers"
import { FormProvider, useForm } from "react-hook-form"

export default requireAuth(function Passport() {
  const { contributorForm, contributorIntro } = styles
  const { ORGANIZATION_NAME, ORGANIZATION_URL, ORGANIZATION_EMAIL, CITY_TOWN, STREET_ADDRESS, ZIP_CODE } = PrimaryInputNames

  const form = useForm()
  const { user } = useAuth()
  const userName = [user.firstName, user.lastName].filter(Boolean).join(" ") || "there"
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const [submitSuccess, setSubmitSuccess] = useState(null)

  async function onSubmit(formValues: any) {
    setLoading(true)
    setSubmitError(null)
    const values = {
      organizationName: formValues[ORGANIZATION_NAME],
      organizationUrl: formValues[ORGANIZATION_URL],
      organizationContact: formValues[ORGANIZATION_EMAIL],
      cityOrTown: formValues[CITY_TOWN],
      streetAddress: formValues[STREET_ADDRESS],
      signupReason: formValues[ResponseTextArea.inputName],
      zipCode: formValues[ZIP_CODE],
      state: formValues[USAStateInput.inputName]
    }
    // TODO: submit form
    // await new Promise((r) => setTimeout(r, 500))
    setLoading(false)
    setSubmitSuccess(`Thank you for your submission:\n${JSON.stringify(values, null, 2)}`)
  }

  function onError(e: any) {
    console.log(e)
  }
  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Contributor Account Application" />
        <p className={contributorIntro}>
          Hello <em>{userName}</em>, thank you for your continued interest in the National Police
          Data Coalition.
          <br />
          <br />
          In order to become a contributor to the Police Data Index, you will need to create or join a contributing organization. Please fill out the form below to get started.
        </p>
        <FormProvider {...form}>
          <form className={contributorForm} onSubmit={form.handleSubmit(onSubmit, onError)}>
            <fieldset>
              <PrimaryInput inputName={ORGANIZATION_NAME} size="large" />
              <PrimaryInput inputName={ORGANIZATION_URL} size="large" />
              <PrimaryInput inputName={ORGANIZATION_EMAIL} size="large" />
              <PrimaryInput inputName={STREET_ADDRESS} size="large" />
              <PrimaryInput inputName={CITY_TOWN} />
              <USAStateInput />
              <PrimaryInput inputName={ZIP_CODE} size="small" />
            </fieldset>
            <ResponseTextArea />
            {submitSuccess ? (
              <SubmissionConfirmation message={submitSuccess} />
            ) : (
              <PrimaryButton loading={loading} type="submit">
                Submit
              </PrimaryButton>
            )}
          </form>
        </FormProvider>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.DASHBOARD} />
      </section>
    </Layout>
  )
})

// TODO: Update to reflect real form submission flow
function SubmissionConfirmation({ message }: { message: any }) {
  return <pre className={styles.submissionConfirmation}>{message}</pre>
}
