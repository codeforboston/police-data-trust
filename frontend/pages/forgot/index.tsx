import React, { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"
import { EnrollmentCallToAction, EnrollmentHeader } from "../../compositions"
import { useAuth, useRedirectOnAuth } from "../../helpers"
import { apiMode } from "../../helpers/api"
import { AppRoutes, CallToActionTypes, PrimaryInputNames } from "../../models"
import { FormLevelError, Layout, PrimaryButton, PrimaryInput } from "../../shared-components"
import sharedStyles from "../../styles/shared.module.css"

const { EMAIL_ADDRESS, PHONE_NUMBER } = PrimaryInputNames

const defaultEmail = apiMode === "mock" ? "test@example.com" : undefined
const defaultPhoneNumber = apiMode === "mock" ? "555 867 5309" : undefined

export default function UserLogin() {
  useRedirectOnAuth(AppRoutes.DASHBOARD)
  const { login } = useAuth()
  const form = useForm()
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)

  async function onSubmit(formValues: any) {
    setLoading(true)
    setSubmitError(null)
    try {
      await login({
        email: formValues[EMAIL_ADDRESS],
        password: formValues[LOGIN_PASSWORD]
      })
    } catch (e) {
      if (e.response?.status === 401) {
        setSubmitError("Couldn't log in. Please check your email and password.")
      } else {
        console.error("Unexpected login error", e)
        setSubmitError("Something went wrong. Please try again.")
      }
    }
    setLoading(false)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Forgot your password?" />
        <FormProvider {...form}>
          <form className={sharedStyles.centerContent} onSubmit={form.handleSubmit(onSubmit)}>
            <PrimaryInput inputName={EMAIL_ADDRESS} defaultValue={defaultEmail} />
            <PrimaryInput inputName={PHONE_NUMBER} defaultValue={defaultPhoneNumber} />
            {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
            <PrimaryButton loading={loading} type="submit">
              Submit
            </PrimaryButton>
            Forgot your Email? <br/>
            Provide Email instead
          </form>
        </FormProvider>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.REMEMBER} />
      </section>
    </Layout>
  )
}
