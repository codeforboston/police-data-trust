import styles from "./passport.module.css"
import { EnrollmentCTA, EnrollmentHeader, USStateSelect } from "../../shared-components"
import { CTATypes } from '../../models'

function handleSubmit() {
  // TODO: add form submission logic
}

export default function Passport({ name = "Herbert Q. Placeholder" }) {
  const {
    cityInput,
    inputWrapper,
    ppForm,
    ppPara,
    ppTextarea,
    ppAddress,
    ppAddInput,
    ppZip,
    ppState,
    ppCity,
    zipInput,
    ppLabel
  } = styles
  return (
    <section className="enrollmentSection">
      <EnrollmentHeader headerText="Passport Account Application"/>
      <p className={ppPara}>Hello <em>{name}</em>, thank you for your continued interest in the National Police Data Coalition.</p>
      <p className={ppPara}>
        We are able to provide access to legally protected data to users with the appropriate permissions. 
        This form will submit your profile for approval.
      </p>
      <form className={ppForm}>
        <fieldset>

        </fieldset>

        <div className={[ppAddress, inputWrapper].join(" ")}>
          <label htmlFor="address" className={styles.label}>Street Address:</label>
          <input type="text" id="address" required={true} className={ppAddInput} />
        </div>
        <div className={[ppCity, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="city" className={ppLabel}>City or Town:</label>
          <input type="text" id="city" required={true} className={cityInput} />
        </div>
        <div className={[ppState, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="state" className={styles.label}>State:</label>
          <USStateSelect />
        </div>
        <div className={[ppZip, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="zip" className={styles.label}>Zip Code:</label>
          <input type="number" id="zip" required={true} className={zipInput} />
        </div>
        <div className={[ppTextarea, inputWrapper].join(" ")}>
          <label htmlFor="textarea" className={ppLabel}>Why are you signing up to the NPDC?:</label>
          <textarea
            id="textarea"
            className={ppTextarea}
            maxLength={500}
            rows={5}
            cols={33}
            required={true}
          />
        </div>
      </form>
      <button className="primaryButton" type="submit" onSubmit={handleSubmit} >
        Submit
      </button>
      <EnrollmentCTA ctaType={CTATypes.DASHBOARD}/>
    </section>
  )
}
