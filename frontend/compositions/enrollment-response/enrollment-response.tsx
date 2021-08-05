import React from 'react'
import Link from 'next/link'
import styles from './enrollment-response.module.css'
import { Logo, ExternalLink } from '../../shared-components'
import { AppRoutes, LogoSizes } from '../../models'

interface EnrollmentResponseProps { isSuccess: boolean }

interface EnrollmentErrorText {
  statusMessage: string,
  returnText: string,
  returnPath: string
}

export enum EnrollmentTypes {
  VIEWER = 'viewer',
  PASSPORT = 'passport'
}

const enrollmentMessage: { [key in EnrollmentTypes]: EnrollmentErrorText} = {
  [EnrollmentTypes.VIEWER]: {
    statusMessage: 'complete your registration',
    returnText: 'Return to login',
    returnPath: AppRoutes.LOGIN
  },
  [EnrollmentTypes.PASSPORT]: {
    statusMessage: 'submit your application',
    returnText: 'Return to dashboard',
    returnPath: AppRoutes.DASHBOARD
  }
}

function failureResponseMessage( enrollmentType: EnrollmentTypes) {
  const { statusMessage, returnText, returnPath } = enrollmentMessage[enrollmentType]
  return (
    <div className={styles.message}>
      <header className={styles.title}>Something went wrong...</header>
      <p>We weren't able to {statusMessage}</p>
      <p className={styles.boldText}>Please come back and try again later</p>
      <p>If the problem perists, please 
        <ExternalLink linkPath="https://github.com/codeforboston/police-data-trust">alert our development team</ExternalLink>
      </p>
      <p>
        <Link href={returnPath}>
          <a>{returnText}</a>
        </Link>
      </p>
    </div>
  )
}

export function RegistrationResponse({ isSuccess }: EnrollmentResponseProps) {
  return (
    <div className={styles.response}>
      <Logo size={LogoSizes.LARGE} />
      {isSuccess ? (
        <div className={styles.message}>
          <header className={styles.title}>Success!</header>
          <p>You have been successfully registered as a Viewer</p>
          <p className={styles.boldText}>Please check your email to confirm your registration</p>
          <p>The confirmation email will direct you to a new login screen</p>
          <p>
            <span className={styles.boldText}>If you need access to legally protected data,</span> you are also invited
            to apply for a <span className={styles.boldText}>Passport Account</span> upon login.
          </p>
        </div>
      ) : failureResponseMessage(EnrollmentTypes.VIEWER)}
    </div>
  )
}

export function PassportApplicationResponse({ isSuccess }: EnrollmentResponseProps) {
  const { returnText, returnPath } = enrollmentMessage[EnrollmentTypes.PASSPORT]
  return (
    <div className={styles.response}>
      <Logo size={LogoSizes.LARGE} />
      {isSuccess ? (
        <div className={styles.message}>
          <header className={styles.title}>Success!</header>
          <p>You have been successfully submitted an application for a Passport account</p>
          <p className={styles.boldText}>Please check your email to confirm your registration</p>
          <p>You can expect to receive a decision in XX days with further instructions. 
            In the meantime, you may continue to explore all public data.
          </p>
          <p>
            <Link href={returnPath}>
              <a>{returnText}</a>
            </Link>
          </p>
        </div>
      ) : failureResponseMessage(EnrollmentTypes.PASSPORT)}
    </div>
  )
}

