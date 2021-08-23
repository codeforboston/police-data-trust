import React, { FormEvent, useState } from "react"
import { EnrollmentCallToAction, EnrollmentHeader } from "../../compositions"
import { CallToActionTypes, PrimaryInputNames } from "../../models"
import { Layout, PrimaryInput } from "../../shared-components"

export default function UserLogin() {
  const { EMAIL_ADDRESS, LOGIN_PASSWORD } = PrimaryInputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Login" />
        <form>
          <PrimaryInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted} />
          <PrimaryInput inputName={LOGIN_PASSWORD} isSubmitted={isSubmitted} />
          <button className="primaryButton" type="submit" onClick={handleSubmit}>
            Submit
          </button>
        </form>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.REGISTER} />
      </section>
    </Layout>
  )
}
