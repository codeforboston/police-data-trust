import React, { FormEvent, useState } from 'react'
import { EnrollmentCTA, EnrollmentHeader, EnrollmentInput } from '../../shared-components'
import { CTATypes, EnrollmentInputNames } from '../../models'

export default function UserLogin() {
  const { EMAIL_ADDRESS, LOGIN_PASSWORD } = EnrollmentInputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <section className="enrollmentSection">
      <EnrollmentHeader headerText="Login"/>
      <form>
        <EnrollmentInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted}/>
        <EnrollmentInput inputName={LOGIN_PASSWORD} isSubmitted={isSubmitted}/>
        <button className="primaryButton" type="submit" onClick={handleSubmit}>
          Submit
        </button>
      </form>
      <EnrollmentCTA ctaType={CTATypes.REGISTER}/>
    </section>
  )
}
