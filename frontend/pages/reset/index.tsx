import React, { useState } from "react"
import { EnrollmentHeader, PasswordAid } from "../../compositions"
import { AppRoutes, CallToActionTypes, PrimaryInputNames, TooltipTypes } from "../../models"
import { Layout, PrimaryInput, PrimaryButton, FormLevelError } from "../../shared-components"
import { useAuth, useRedirectOnAuth } from "../../helpers"
import { resetPassword } from "../../helpers/api"
import { FormProvider, useForm } from "react-hook-form"
import { useRouter } from "next/router"

const { CREATE_PASSWORD, CONFIRM_PASSWORD } =
  PrimaryInputNames
const passwordAidId = "passwordAid"

export default function ResetPassword() {
  const router = useRouter()
  const token = router.query.token instanceof Array ? router.query.token[0] : router.query.token
  
  useRedirectOnAuth(AppRoutes.DASHBOARD)
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
      await resetPassword({
        password: formValues[CREATE_PASSWORD],
        token,
      })
    } catch (e) {
      console.error("Unexpected registration error", e)
      setSubmitError("Something went wrong. Please try again.")
    }
    setLoading(false)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Register: Viewer Account" tooltip={TooltipTypes.VIEWER} />
        <FormProvider {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <PrimaryInput inputName={CREATE_PASSWORD} isShown={isPasswordShown} />
            <PrimaryInput inputName={CONFIRM_PASSWORD} isShown={isPasswordShown} />
            <PasswordAid id={passwordAidId} onDisplayChange={handlePasswordDisplay} />
            {submitError && <FormLevelError errorId="submitError" errorMessage={submitError} />}
            <PrimaryButton loading={loading} type="submit">
              Submit
            </PrimaryButton>
          </form>
        </FormProvider>
      </section>
    </Layout>
  )
}
