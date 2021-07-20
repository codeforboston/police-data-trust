import React, { FormEvent, useState } from "react"
import styles from "./passport.module.css"
import { 
  ResponseTextArea, EnrollmentCTA, EnrollmentHeader, EnrollmentInput, USStateSelect 
} from "../../shared-components"
import { CTATypes, EnrollmentInputNames } from '../../models'

export default function Passport({ name = ['Herbert Placeholder'] }) {
  const { passportForm, passportIntro } = styles
  const { CITY_TOWN, STREET_ADDRESS, ZIP_CODE } = EnrollmentInputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    // TODO: add form submission logic
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <section className="enrollmentSection">
      <EnrollmentHeader headerText="Passport Account Application"/>
      <p className={passportIntro}>
        Hello <em>{name}</em>, thank you for your continued interest in the National Police Data Coalition.<br/><br/>
        We are able to provide access to legally protected data to users with the appropriate permissions. 
        This form will submit your profile for approval.
      </p>
      <form className={passportForm}>
        <fieldset>
          <EnrollmentInput inputName={STREET_ADDRESS} size="large" isSubmitted={isSubmitted}/>
          <EnrollmentInput inputName={CITY_TOWN} isSubmitted={isSubmitted}/>
          <USStateSelect isSubmitted={isSubmitted} />
          <EnrollmentInput inputName={ZIP_CODE} size="small" isSubmitted={isSubmitted}/>
        </fieldset>
        <ResponseTextArea isSubmitted={isSubmitted} />
        <button className="primaryButton" type="submit" onClick={handleSubmit}>
          Submit
        </button>
      </form>
      <EnrollmentCTA ctaType={CTATypes.DASHBOARD}/>
    </section>
  )
}
