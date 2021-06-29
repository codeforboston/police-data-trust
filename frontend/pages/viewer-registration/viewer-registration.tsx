import React, { FormEvent, useState } from 'react'
import styles from './viewer-registration.module.css'
import PasswordAid from './password-aid/password-aid'
import { EnrollmentCTA, EnrollmentHeader, TextInput } from '../../shared-components'
import { CTATypes, InputNames, TooltipTypes } from '../../models'

export default function ViewerRegistration() {  
  const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } = InputNames
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
    <section className={registration}>
      <EnrollmentHeader
        headerText="Register: Viewer Account" 
        tooltip={TooltipTypes.VIEWER}
      />
      <form>
        <fieldset className={inputLine}>
          <TextInput inputName={FIRST_NAME} isSubmitted={isSubmitted}/>
          <TextInput inputName={LAST_NAME} isSubmitted={isSubmitted}/>
        </fieldset>
        <fieldset className={inputLine}>
          <TextInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted}/>
          <TextInput inputName={PHONE_NUMBER} isSubmitted={isSubmitted}/>
        </fieldset>
        <fieldset className={inputLine} aria-describedby={passwordAidId}>
          <TextInput inputName={CREATE_PASSWORD} isSubmitted={isSubmitted} isPasswordShown={isPasswordShown}/>
          <TextInput inputName={CONFIRM_PASSWORD} isSubmitted={isSubmitted}/>
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
