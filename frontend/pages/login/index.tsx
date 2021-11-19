import React, { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"
import { EnrollmentCallToAction, EnrollmentHeader } from "../../compositions"
import { useAuth, useRedirectOnAuth } from "../../helpers"
import { apiMode } from "../../helpers/api"
import { AppRoutes, CallToActionTypes, PrimaryInputNames } from "../../models"
import { FormLevelError, Layout, PrimaryButton, PrimaryInput } from "../../shared-components"
import sharedStyles from "../../styles/shared.module.css"

const { EMAIL_ADDRESS, LOGIN_PASSWORD } = PrimaryInputNames

const defaultEmail = apiMode === "mock" ? "test@example.com" : undefined
const defaultPassword = apiMode === "mock" ? "password" : undefined

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
        <EnrollmentHeader headerText="Login" />
        <FormProvider {...form}>
          <form className={sharedStyles.centerContent} onSubmit={form.handleSubmit(onSubmit)}>
            <PrimaryInput inputName={EMAIL_ADDRESS} defaultValue={defaultEmail} />
            <PrimaryInput inputName={LOGIN_PASSWORD} defaultValue={defaultPassword} />
            <EnrollmentCallToAction callToActionType={CallToActionTypes.FORGOT} />
            {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
            <PrimaryButton loading={loading} type="submit">
              Submit
            </PrimaryButton>
          </form>
        </FormProvider>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.REGISTER} />
      </section>
    </Layout>
  )
}
