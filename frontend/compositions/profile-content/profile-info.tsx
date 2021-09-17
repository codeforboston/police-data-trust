import * as React from "react"
import styles from "./profile-content.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEdit } from "@fortawesome/free-solid-svg-icons"
import { UserProfileProps, emptyUser } from "../../models/profile"
import { PrimaryInputNames } from "../../models"
import { PrimaryInput } from "../../shared-components"

export default function ProfileInfo({ userData = emptyUser }: UserProfileProps) {
  const [editMode, setEditMode] = React.useState(false)
  const [isSubmitted, setIsSubmitted] = React.useState(false)

  const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } =
    PrimaryInputNames

  const { profileData, sectionTitle, row } = styles
  const { firstName, lastName, email, phone } = userData

  function handleSubmit($event: React.FormEvent<HTMLButtonElement>) {
    // TODO: validate input, update user
    $event.preventDefault()
    setIsSubmitted(true)
  }

  if (editMode) {
    const { inputLine, formControls, cancelButton, submitButton } = styles
    return (
      <div className={profileData}>
        <header className={sectionTitle}>Edit Your Account Information</header>
        <form>
          <fieldset className={inputLine}>
            <PrimaryInput inputName={FIRST_NAME} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={LAST_NAME} isSubmitted={isSubmitted} />
          </fieldset>
          <fieldset className={inputLine}>
            <PrimaryInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={PHONE_NUMBER} isSubmitted={isSubmitted} />
          </fieldset>
          <fieldset className={inputLine}>
            <PrimaryInput inputName={CREATE_PASSWORD} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={CONFIRM_PASSWORD} isSubmitted={isSubmitted} />
          </fieldset>
          <div className={formControls}>
            <button className={cancelButton} onClick={() => setEditMode(false)}>
              Cancel
            </button>
            <button className={submitButton} onClick={handleSubmit}>
              Save Changes
            </button>
          </div>
        </form>
      </div>
    )
  } else {
    const { editButton, dataView, dataCell, dataBreak, label, dataField } = styles
    return (
      <div className={profileData}>
        <header className={sectionTitle}>
          Your Account Information
          <FontAwesomeIcon
            icon={faEdit}
            size="1x"
            className={editButton}
            onClick={() => setEditMode(true)}
          />
        </header>
        <main className={dataView}>
          <div className={dataCell}>
            <div className={label}>First name:</div>
            <div className={dataField}>{firstName}</div>
          </div>
          <div className={dataCell}>
            <div className={label}>Last name:</div>
            <div className={dataField}>{lastName}</div>
          </div>
          <div className={dataBreak}></div>
          <div className={dataCell}>
            <div className={label}>Email address:</div>
            <div className={dataField}>{email}</div>
          </div>
          <div className={dataCell}>
            <div className={label}>Phone number:</div>
            <div className={dataField}>{formatPhoneNumber(phone)}</div>
          </div>
        </main>
      </div>
    )
  }
}

// format as (999) 999-9999
function formatPhoneNumber(rawPhoneNumber: string) {
  const cleaned = ("" + rawPhoneNumber).replace(/\D/g, "")
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
  return match ? `(${match[1]}) ${match[2]}-${match[3]}` : "--"
}
