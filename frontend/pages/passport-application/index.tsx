import Link from "next/link"

import Logo from "../../shared-components/logo"
import styles from "./passport.module.css"
import { USStateSelect } from "../../shared-components/state-select/UsStateSelect"

function handleSubmit() {
  // TODO: add form submission logic
}

export default function Passport({ name = "Herbert Q. Placeholder" }) {
  const {
    ppWrapper,
    cityInput,
    logoWrapper,
    inputWrapper,
    ppForm,
    ppHeading,
    ppParaWrapper,
    ppPara,
    ppRedirect,
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
    <div className={ppWrapper}>
      <div className={logoWrapper}>
        <Logo />
      </div>
      <h1 className={ppHeading}>Passport Account Application</h1>
      <div className={ppParaWrapper}>
        <p className={ppPara}>
          Hello <em>{name}</em>, thank you for your continued interest in the National Police Data
          Coalition.
        </p>
        <p className={ppPara}>
          We are able to provide access to legally protected data to users with the appropriate
          permissions. This form will submit your profile for approval.
        </p>
      </div>
      <form className={ppForm}>
        <div className={[ppAddress, inputWrapper].join(" ")}>
          <label htmlFor="address" className={styles.label}>
            <strong>Street Address:</strong>
          </label>
          <input type="text" id="address" required={true} className={ppAddInput} />
        </div>
        <div className={[ppCity, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="city" className={ppLabel}>
            <strong>City or Town:</strong>
          </label>
          <input type="text" id="city" required={true} className={cityInput} />
        </div>
        <div className={[ppState, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="state" className={styles.label}>
            <strong>State:</strong>
          </label>
          <USStateSelect />
        </div>
        <div className={[ppZip, inputWrapper].join(" ")}>
          {" "}
          <label htmlFor="zip" className={styles.label}>
            <strong>Zip Code:</strong>
          </label>
          <input type="number" id="zip" required={true} className={zipInput} />
        </div>
        <div className={[ppTextarea, inputWrapper].join(" ")}>
          <label htmlFor="textarea" className={ppLabel}>
            <strong>Why are you signing up to the NPDC?:</strong>
          </label>
          <textarea
            id="textarea"
            className={ppTextarea}
            defaultValue="I want to sign up for the NPDC because..."
            maxLength={500}
            rows={5}
            cols={33}
            required={true}
          />
        </div>
      </form>
      <button type="submit" onSubmit={handleSubmit} className="primaryButton">
        Submit
      </button>
      <div className={ppRedirect}>
        <Link href="/dashboard">
          <a>Return to dashboard</a>
        </Link>
      </div>
    </div>
  )
}
