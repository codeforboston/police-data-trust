import styles from "./passport.module.css"
import { 
  ApplicationResponse, EnrollmentCTA, EnrollmentHeader, EnrollmentInput, USStateSelect 
} from "../../shared-components"
import { CTATypes, EnrollmentInputNames } from '../../models'

export default function Passport({ name = ['Herbert', 'Placeholder'] }) {
  const { passportForm, passportIntro } = styles
  const { CITY_TOWN, STREET_ADDRESS, ZIP_CODE } = EnrollmentInputNames

  function handleSubmit() {
    // TODO: add form submission logic
  }

  return (
    <section className="enrollmentSection">
      <EnrollmentHeader headerText="Passport Account Application"/>
      <p className={passportIntro}>
        Hello {name.join(' ')}, thank you for your continued interest in the National Police Data Coalition.<br/><br/>
        We are able to provide access to legally protected data to users with the appropriate permissions. 
        This form will submit your profile for approval.
      </p>
      <form className={passportForm}>
        <fieldset>
          <EnrollmentInput inputName={STREET_ADDRESS} isSubmitted={false} size="large"/>
          <EnrollmentInput inputName={CITY_TOWN} isSubmitted={false} />
          <USStateSelect />
          <EnrollmentInput inputName={ZIP_CODE} isSubmitted={false} size="small"/>
        </fieldset>
        <ApplicationResponse />
        <button className="primaryButton" type="submit" onSubmit={handleSubmit}>
          Submit
        </button>
      </form>
      <EnrollmentCTA ctaType={CTATypes.DASHBOARD}/>
    </section>
  )
}
