import React, { FormEvent, useState } from 'react'
import styles from './user-login.module.css'
import { EnrollmentCTA, EnrollmentHeader, TextInput } from '../../shared-components'
import { CTATypes, InputNames } from '../../models'

export default function UserLogin() {
  const { EMAIL_ADDRESS, LOGIN_PASSWORD } = InputNames

  const [isSubmitted, setIsSubmitted] = useState(false)

  function handleSubmit($event: FormEvent<HTMLButtonElement>): void {
    $event.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <section className={styles.login}>
      <EnrollmentHeader headerText="Login"/>
      <form>
        <TextInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted}/>
        <TextInput inputName={LOGIN_PASSWORD} isSubmitted={isSubmitted}/>
        <button className="primaryButton" type="submit" onClick={handleSubmit}>
          Submit
        </button>
      </form>
      <EnrollmentCTA ctaType={CTATypes.REGISTER}/>
    </section>
  )
}
