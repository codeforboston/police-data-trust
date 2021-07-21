import React, { FormEvent, useState } from 'react'
import styles from './viewer-registration.module.css'
<<<<<<< HEAD:frontend/pages/viewer-registration/index.tsx
import PasswordAid from '../../shared-components/password-aid/password-aid'
import { EnrollmentCTA, EnrollmentHeader, TextInput } from '../../shared-components'
import { CTATypes, InputNames, TooltipTypes } from '../../models'
=======
import PasswordAid from './password-aid/password-aid'
import { EnrollmentCTA, EnrollmentHeader, EnrollmentInput } from '../../shared-components'
import { CTATypes, EnrollmentInputNames, TooltipTypes } from '../../models'
>>>>>>> 843f2c8dd82cf6da1476db3c31aaa6346120ec6a:frontend/pages/register/index.tsx

export default function ViewerRegistration() {  
  const { 
    FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD 
  } = EnrollmentInputNames
  const { registration, inputLine } = styles
  const passwordAidId: string = 'passwordAid'
  
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
    <section className="enrollmentSection">
      <EnrollmentHeader
        headerText="Register: Viewer Account" 
        tooltip={TooltipTypes.VIEWER}
      />
      <form>
        <fieldset className={inputLine}>
          <EnrollmentInput inputName={FIRST_NAME} isSubmitted={isSubmitted}/>
          <EnrollmentInput inputName={LAST_NAME} isSubmitted={isSubmitted}/>
        </fieldset>
        <fieldset className={inputLine}>
          <EnrollmentInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted}/>
          <EnrollmentInput inputName={PHONE_NUMBER} isSubmitted={isSubmitted}/>
        </fieldset>
        <fieldset className={inputLine} aria-describedby={passwordAidId}>
          <EnrollmentInput inputName={CREATE_PASSWORD} isSubmitted={isSubmitted} isShown={isPasswordShown}/>
          <EnrollmentInput inputName={CONFIRM_PASSWORD} isSubmitted={isSubmitted}/>
        </fieldset>
        <PasswordAid id={passwordAidId} onDisplayChange={handlePasswordDisplay}/>
        <button className="primaryButton" type="submit" onClick={handleSubmit}>
          Submit
        </button>
      </form>
      <EnrollmentCTA ctaType={CTATypes.LOGIN}/>
    </section>
  )
}
