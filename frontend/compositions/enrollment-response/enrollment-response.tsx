import React from "react"
import Link from "next/link"
import styles from "./enrollment-response.module.css"
import { Logo, ExternalLink } from "../../shared-components"
import { EnrollmentTypes, enrollmentMessage, LogoSizes } from "../../models"
export interface ResponseProps {
  success?: boolean
}

function failureResponseMessage(enrollmentType: EnrollmentTypes) {
  const { statusMessage, returnText, returnPath } = enrollmentMessage[enrollmentType]
  const { message, title, boldText } = styles
  return (
    <div className={message}>
      <header className={title}>Something went wrong...</header>
      <p>We weren&apos;t able to {statusMessage}</p>
      <p className={boldText}>Please come back and try again later</p>
      <p>
        If the problem perists, please
        <ExternalLink
          linkPath="https://github.com/codeforboston/police-data-trust"
          linkText="alert our development team"
        />
      </p>
      <p>
        <Link href={returnPath}>
          <a>{returnText}</a>
        </Link>
      </p>
    </div>
  )
}

export function RegistrationResponse(props: ResponseProps) {
  const { response, message, title, boldText } = styles
  const { success } = props
  return (
    <div className={response}>
      <Logo size={LogoSizes.LARGE} />
      {success ? (
        <div className={message}>
          <header className={title}>Success!</header>
          <p>You have been successfully registered as a Viewer</p>
          <p className={boldText}>Please check your email to confirm your registration</p>
          <p>The confirmation email will direct you to a new login screen</p>
          <p>
            <span className={boldText}>If you need access to legally protected data,</span> you are
            also invited to apply for a <span className={boldText}>Passport Account</span> upon
            login.
          </p>
        </div>
      ) : (
        failureResponseMessage(EnrollmentTypes.VIEWER)
      )}
    </div>
  )
}

export function PassportApplicationResponse(props: ResponseProps) {
  const { returnText, returnPath } = enrollmentMessage[EnrollmentTypes.PASSPORT]
  const { response, message, title, boldText } = styles
  const { success } = props
  return (
    <div className={response}>
      <Logo size={LogoSizes.LARGE} />
      {success ? (
        <div className={message}>
          <header className={title}>Success!</header>
          <p>You have successfully submitted an application for a Passport account</p>
          <p className={boldText}>Please check your email to confirm your registration</p>
          <p>
            You can expect to receive a decision in XX days with further instructions. In the
            meantime, you may continue to explore all public data.
          </p>
          <p>
            <Link href={returnPath}>
              <a>{returnText}</a>
            </Link>
          </p>
        </div>
      ) : (
        failureResponseMessage(EnrollmentTypes.PASSPORT)
      )}
    </div>
  )
}
