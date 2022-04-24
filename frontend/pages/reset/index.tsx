import React, { useState } from "react"
import { EnrollmentHeader, PasswordAid } from "../../compositions"
import { AppRoutes, PrimaryInputNames } from "../../models"
import { Layout, PrimaryInput, PrimaryButton, FormLevelError } from "../../shared-components"
import styles from "./reset.module.css"
import { useRedirectOnAuth } from "../../helpers"
import { resetPassword } from "../../helpers/api"
import { FormProvider, useForm } from "react-hook-form"
import { useRouter } from "next/router"

const { CREATE_PASSWORD, CONFIRM_PASSWORD } = PrimaryInputNames
const passwordAidId = "passwordAid"

export default function ResetPassword() {
  const router = useRouter()
  const token = router.query.token instanceof Array ? router.query.token[0] : router.query.token

  useRedirectOnAuth(AppRoutes.LOGIN)

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
        accessToken: token
      })
      router.push(AppRoutes.LOGIN)
    } catch (e) {
      console.warn("Unexpected password reset error", e.message)
      if (e.message.includes("401")) {
        setSubmitError("Token Invalid, please request another forgot password email.")
      } else {
        setSubmitError("Something went wrong. Please try again.")
      }
    }
    setLoading(false)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Reset Password" />
        <FormProvider {...form}>
          <form className={styles.form} onSubmit={form.handleSubmit(onSubmit)}>
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
