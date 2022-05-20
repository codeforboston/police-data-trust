import React, { useState } from "react"
import styles from "./edit-info.module.css"
import { PrimaryInputNames } from "../../models"
import { Layout, PrimaryInput, PrimaryButton, FormLevelError } from "../../shared-components"
import { useAuth } from "../../helpers"
import { FormProvider, useForm } from "react-hook-form"

interface EditProfileProps {
  cancelEditMode: any
}

export default function EditProfileInfo({ cancelEditMode }: EditProfileProps) {
  const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } =
    PrimaryInputNames

  const form = useForm()
  const { user } = useAuth()

  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const [submitSuccess, setSubmitSuccess] = useState(null)

  // TODO: should only submit updated fields - ideally a PATCH request
  async function onSubmit(formValues: any) {
    setLoading(true)
    setSubmitError(null)
    const values = {
      firstName: formValues[FIRST_NAME],
      lastName: formValues[LAST_NAME],
      emailAddress: formValues[EMAIL_ADDRESS],
      phoneNumber: formValues[PHONE_NUMBER],
      createPw: formValues[CREATE_PASSWORD],
      confirmPw: formValues[CONFIRM_PASSWORD]
    }
    // TODO: submit form
    setLoading(false)
    setSubmitSuccess(`Your profile has been updated:\n${JSON.stringify(values, null, 2)}`)
  }

  function onError(e: any) {
    setSubmitError(e)
  }

  const { profileData, sectionTitle, inputLine, formControls, cancelButton, submitButton } = styles

  return (
    <Layout>
      <div className={profileData}>
        <header className={sectionTitle}>Edit Your Account Information</header>
        <FormProvider {...form}>
          <form onSubmit={form.handleSubmit(onSubmit, onError)}>
            <fieldset className={inputLine}>
              <PrimaryInput inputName={FIRST_NAME} />
              <PrimaryInput inputName={LAST_NAME} />
            </fieldset>
            <fieldset className={inputLine}>
              <PrimaryInput inputName={EMAIL_ADDRESS} />
              <PrimaryInput inputName={PHONE_NUMBER} />
            </fieldset>
            <fieldset className={inputLine}>
              <PrimaryInput inputName={CREATE_PASSWORD} />
              <PrimaryInput inputName={CONFIRM_PASSWORD} />
            </fieldset>
            {submitSuccess ? (
              <SubmissionConfirmation message={submitSuccess} />
            ) : (
              <div className={formControls}>
                <button className={cancelButton} onClick={cancelEditMode}>
                  Cancel
                </button>
                <PrimaryButton loading={loading} type="submit" className={submitButton}>
                  Save
                </PrimaryButton>
              </div>
            )}
          </form>
        </FormProvider>
      </div>
    </Layout>
  )
}

// TODO: Update to reflect real form submission flow
function SubmissionConfirmation({ message }: { message: any }) {
  return <pre className={styles.submissionConfirmation}>{message}</pre>
}
