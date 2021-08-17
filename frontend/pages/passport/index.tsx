import React, { FormEvent, useState } from "react"
import styles from "./passport.module.css"
import { EnrollmentCallToAction, EnrollmentHeader } from '../../compositions'
import { CallToActionTypes, PrimaryInputNames } from "../../models"
import { Layout, PrimaryInput, ResponseTextArea, USAStateInput } from "../../shared-components"

export default function Passport({ name = ["Herbert Placeholder"] }) {
  const { passportForm, passportIntro } = styles
  const { CITY_TOWN, STREET_ADDRESS, ZIP_CODE } = PrimaryInputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    // TODO: add form submission logic
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <Layout>
      <section className="enrollmentSection">
        <EnrollmentHeader headerText="Passport Account Application"/>
        <p className={passportIntro}>
          Hello <em>{name}</em>, thank you for your continued interest in the National Police Data Coalition.<br/><br/>
          We are able to provide access to legally protected data to users with the appropriate permissions. 
          This form will submit your profile for approval.
        </p>
        <form className={passportForm}>
          <fieldset>
            <PrimaryInput inputName={STREET_ADDRESS} size="large" isSubmitted={isSubmitted}/>
            <PrimaryInput inputName={CITY_TOWN} isSubmitted={isSubmitted}/>
            <USAStateInput isSubmitted={isSubmitted} />
            <PrimaryInput inputName={ZIP_CODE} size="small" isSubmitted={isSubmitted}/>
          </fieldset>
          <ResponseTextArea isSubmitted={isSubmitted} />
          <button className="primaryButton" type="submit" onClick={handleSubmit}>
            Submit
          </button>
        </form>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.DASHBOARD}/>
      </section>
    </Layout>
  )
}
