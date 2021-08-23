import React, { FormEvent, useState } from "react"
import styles from "./viewer-registration.module.css"

import { EnrollmentCallToAction, EnrollmentHeader, PasswordAid } from "../../compositions"
import { CallToActionTypes, PrimaryInputNames, TooltipTypes } from "../../models"
import { Layout, PrimaryInput } from "../../shared-components"

export default function ViewerRegistration() {
  const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } =
    PrimaryInputNames
  const { inputLine } = styles
  const passwordAidId: string = "passwordAid"

  const [isSubmitted, setIsSubmitted] = useState(false)
  const [isPasswordShown, setIsPasswordShown] = useState(false)

  function handlePasswordDisplay(): void {
    setIsPasswordShown(!isPasswordShown)
  }

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    // TODO: handle form submission - set input values to state onChange
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Register: Viewer Account" tooltip={TooltipTypes.VIEWER} />
        <form>
          <fieldset className={inputLine}>
            <PrimaryInput inputName={FIRST_NAME} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={LAST_NAME} isSubmitted={isSubmitted} />
          </fieldset>
          <fieldset className={inputLine}>
            <PrimaryInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={PHONE_NUMBER} isSubmitted={isSubmitted} />
          </fieldset>
          <fieldset className={inputLine} aria-describedby={passwordAidId}>
            <PrimaryInput
              inputName={CREATE_PASSWORD}
              isSubmitted={isSubmitted}
              isShown={isPasswordShown}
            />
            <PrimaryInput inputName={CONFIRM_PASSWORD} isSubmitted={isSubmitted} />
          </fieldset>
          <PasswordAid id={passwordAidId} onDisplayChange={handlePasswordDisplay} />
          <button className="primaryButton" type="submit" onClick={handleSubmit}>
            Submit
          </button>
        </form>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.LOGIN} />
      </section>
    </Layout>
  )
}
