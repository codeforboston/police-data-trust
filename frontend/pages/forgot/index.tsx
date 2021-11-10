import { faClosedCaptioning } from "@fortawesome/free-regular-svg-icons"
import React, { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"
import { EnrollmentCallToAction, EnrollmentHeader } from "../../compositions"
import { useAuth, useRedirectOnAuth } from "../../helpers"
import { apiMode } from "../../helpers/api"
import { AppRoutes, CallToActionTypes, PrimaryInputNames } from "../../models"
import { FormLevelError, Layout, PrimaryButton, LinkButton, PrimaryInput } from "../../shared-components"
import sharedStyles from "../../styles/shared.module.css"

const { EMAIL_ADDRESS, PHONE_NUMBER } = PrimaryInputNames

const defaultEmail = apiMode === "mock" ? "test@example.com" : undefined
const defaultPhoneNumber = apiMode === "mock" ? "555 867 5309" : undefined

export default function ForgotPassword() {
  useRedirectOnAuth(AppRoutes.DASHBOARD)
  const { login } = useAuth()
  const form = useForm()
  const [loading, setLoading] = useState(false)
  const [submitError, setSubmitError] = useState(null)
  const [useEmail, setEmailState] = useState(true) //true when using email, false when using phone number

  async function onSubmit(formValues: any) {
    setLoading(true)
    setSubmitError(null)
    try {
      if(useEmail){
        //find password using email
        setSubmitError("Email not connected to back end")
      }
      else{
        //find password using phone number
        setSubmitError("Phone number not connected to back end")
      }
    } catch (e) {

    }
    setLoading(false)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Forgot your password?" />
        <FormProvider {...form}>
          <form className={sharedStyles.centerContent} onSubmit={form.handleSubmit(onSubmit)}>
            <PrimaryInput inputName={EMAIL_ADDRESS} defaultValue={defaultEmail} className={useEmail ? "" : "hidden"} />
            <PrimaryInput inputName={PHONE_NUMBER} defaultValue={defaultPhoneNumber} className={useEmail ? "hidden" : ""} />
            {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
            <PrimaryButton loading={loading} type="submit">
              Submit
            </PrimaryButton>
          </form>
          <LinkButton loading={loading} type="forgot_toPhone" className={useEmail ? "" : "hidden"} onClick={() =>{setEmailState(false)}}>
            Forgot your Email?
          </LinkButton>
          <LinkButton loading={loading} type="forgot_toEmail" className={useEmail ? "hidden" : ""} onClick={() =>{setEmailState(true)}}>
            Provide Email instead
          </LinkButton>
        </FormProvider>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.REMEMBER} />
      </section>
    </Layout>
  )
}
