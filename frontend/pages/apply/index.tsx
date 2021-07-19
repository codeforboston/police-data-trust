import styles from "./passport.module.css"
import { EnrollmentCTA, EnrollmentHeader, EnrollmentInput, USStateSelect } from "../../shared-components"
import { CTATypes, EnrollmentInputNames } from '../../models'

function handleSubmit() {
  // TODO: add form submission logic
}

export default function Passport({ name = ['Herbert', 'Placeholder'] }) {
  const { passportForm, passportIntro } = styles
  const { CITY_TOWN, STREET_ADDRESS, ZIP_CODE } = EnrollmentInputNames

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
          <EnrollmentInput inputName={STREET_ADDRESS} isSubmitted={false} />
          <EnrollmentInput inputName={CITY_TOWN} isSubmitted={false} />
          <USStateSelect />
          <EnrollmentInput inputName={ZIP_CODE} isSubmitted={false} />
        </fieldset>
        <label htmlFor="interestDescription">
          Why are you signing up to the NPDC?:
        </label>
        <textarea
          id="interestDescription"
          maxLength={500}
          rows={5}
          cols={33}
          aria-required="true"
        />
      </form>
      <button className="primaryButton" type="submit" onSubmit={handleSubmit} >
        Submit
      </button>
      <EnrollmentCTA ctaType={CTATypes.DASHBOARD}/>
    </section>
  )
}
