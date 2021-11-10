import React, { FormEvent, useState } from "react"
import styles from "./viewer-registration.module.css"

import { EnrollmentCallToAction, EnrollmentHeader, PasswordAid } from "../../compositions"
import { AppRoutes, CallToActionTypes, PrimaryInputNames, TooltipTypes } from "../../models"
import { Layout, PrimaryInput, PrimaryButton, FormLevelError } from "../../shared-components"
import { useAuth, useRedirectOnAuth } from "../../helpers"
import { FormProvider, useForm } from "react-hook-form"
import { AxiosError, AxiosResponse } from "axios"

const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } =
  PrimaryInputNames
const { inputLine } = styles
const passwordAidId = "passwordAid"

export default function ViewerRegistration() {
  useRedirectOnAuth(AppRoutes.DASHBOARD)
  const { register } = useAuth()
  const form = useForm()
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const [isPasswordShown, setIsPasswordShown] = useState(false)

  function handlePasswordDisplay(): void {
    setIsPasswordShown(!isPasswordShown)
  }

  async function onSubmit(formValues: any) {
    if (formValues[CREATE_PASSWORD] !== formValues[CONFIRM_PASSWORD]) {
      form.setError(CONFIRM_PASSWORD, { message: "Passwords do not match", type: "validate" })
      return
    }

    setLoading(true)
    setSubmitError(null)
    try {
      await register({
        firstName: formValues[FIRST_NAME],
        lastName: formValues[LAST_NAME],
        email: formValues[EMAIL_ADDRESS],
        password: formValues[CREATE_PASSWORD],
        phoneNumber: formValues[PHONE_NUMBER]
      })
    } catch (e) {
      if (existingAccount(e)) {
        setSubmitError("Existing account found. Please use a different email address.")
      } else {
        console.error("Unexpected registration error", e)
        setSubmitError("Something went wrong. Please try again.")
      }
    }
    setLoading(false)
  }

  function existingAccount(e?: AxiosError) {
    return (
      e.response?.status === 400 &&
      e.response?.data?.message?.match(/email matches existing account/i)
    )
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Register: Viewer Account" tooltip={TooltipTypes.VIEWER} />
        <FormProvider {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <fieldset className={inputLine}>
              <PrimaryInput inputName={FIRST_NAME} />
              <PrimaryInput inputName={LAST_NAME} />
            </fieldset>
            <fieldset className={inputLine}>
              <PrimaryInput inputName={EMAIL_ADDRESS} />
              <PrimaryInput inputName={PHONE_NUMBER} />
            </fieldset>
            <fieldset className={inputLine} aria-describedby={passwordAidId}>
              <PrimaryInput inputName={CREATE_PASSWORD} isShown={isPasswordShown} />
              <PrimaryInput inputName={CONFIRM_PASSWORD} isShown={isPasswordShown} />
            </fieldset>
            <PasswordAid id={passwordAidId} onDisplayChange={handlePasswordDisplay} />
            {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
            <PrimaryButton loading={loading} type="submit">
              Submit
            </PrimaryButton>
          </form>
        </FormProvider>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.LOGIN} />
      </section>
    </Layout>
  )
}
