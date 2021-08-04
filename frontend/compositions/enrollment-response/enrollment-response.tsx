import styles from './enrollment-response.module.css'
import { Logo } from '../../shared-components'
import { EnrollmentTypes, CallToActionTypes } from '../../models'
import { EnrollmentCallToAction } from '../../compositions'

interface EnrollmentResponseProps { 
  isSuccess: boolean, 
  enrollmentType: EnrollmentTypes 
}

export default function RegistrationResponse({ isSuccess, enrollmentType }: EnrollmentResponseProps) {
  switch (enrollmentType) {
    case EnrollmentTypes.VIEWER:
      return isSuccess ? ViewerRegistrationSuccessResponse() : ViewerRegistrationFailureResponse()
    case EnrollmentTypes.PASSPORT:
      return isSuccess ? PassportApplicationSuccessResponse() : PassportApplicationFailureResponse()
  }
}


function ViewerRegistrationSuccessResponse() {
  return (
    <div className={styles.response}>
      <Logo />
      <h1 className={styles.title}>Success!</h1>
      <div className={styles.content}>
        <p>You have been successfully registered as a Viewer</p>
        <p><b>Please check your email to confirm your registration</b></p>
        <p>The confirmation email will direct you to a new login screen</p>
        <p>
          <b>If you need access to legally protected data,</b> you are also invited
          to apply for a <b>Passport Account</b> upon login.
        </p>
      </div>
    </div>
  )
}

function ViewerRegistrationFailureResponse() {
  return (
    <div className={styles.response}>
      <Logo />
      <h1 className={styles.title}>Something went wrong...</h1>
      <div className={styles.content}>
        <p>We weren't able to complete your registration.</p>
        <p><b>Please come back and try again later</b></p>
        <p>If the problem persists, <a className={styles.externalLink} href="">please alert our development team</a></p>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.LOGIN} />
      </div>
    </div>
  )
}

function PassportApplicationSuccessResponse() {
  return (
    <div className={styles.response}>
      <Logo />
      <h1 className={styles.title}>Success!</h1>
      <div className={styles.content}>
        <p>You have been successfully submitted an application for a Passport account</p>
        <p><b>Please check your email to confirm your registration</b></p>
        <p>You can expect to receive a decision in XX days with further instructions. 
          In the meantime, you may continue to explore all public data.
        </p>

      </div>
    </div>
  )
}


function PassportApplicationFailureResponse() {
  return (
    <div className={styles.response}>
      <Logo />
      <h1 className={styles.title}>Something went wrong...</h1>
      <div className={styles.content}>
        <p>We weren't able to submit your application.</p>
        <p><b>Please come back and try again later</b></p>
        <p>If the problem persists, <a className={styles.externalLink} href="">please alert our development team</a></p>
        <EnrollmentCallToAction callToActionType={CallToActionTypes.DASHBOARD} />
      </div>
    </div>
  )
}