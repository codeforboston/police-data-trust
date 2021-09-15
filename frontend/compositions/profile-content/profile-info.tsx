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

  const { FIRST_NAME, LAST_NAME, EMAIL_ADDRESS, PHONE_NUMBER, CREATE_PASSWORD, CONFIRM_PASSWORD } = PrimaryInputNames
  
  const { profileData, sectionTitle, row } = styles
  const { firstName, lastName, email, phone } = userData

  function handleSubmit($event: React.FormEvent<HTMLButtonElement>) {
    // TODO: validate input, update user
    $event.preventDefault()
    setIsSubmitted(true)
  }

  if (editMode) {
    return (
      <div className={profileData}>
        <header className={sectionTitle}>Edit Your Account Information</header>
        <form>
          <div className={row}>
            <PrimaryInput inputName={FIRST_NAME} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={LAST_NAME} isSubmitted={isSubmitted} />
          </div>
          <div className={row}>
            <PrimaryInput inputName={EMAIL_ADDRESS} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={PHONE_NUMBER} isSubmitted={isSubmitted} />
          </div>
          <div className={row}>
            <PrimaryInput inputName={CREATE_PASSWORD} isSubmitted={isSubmitted} />
            <PrimaryInput inputName={CONFIRM_PASSWORD} isSubmitted={isSubmitted} />
          </div>
          <div className={row}>
            <button className={styles.cancelButton} onClick={() => setEditMode(false)}>
              Cancel
            </button>
            <button className={styles.submitButton} onClick={handleSubmit}>Save Changes</button>
          </div>
        </form>
      </div>
    )
  } else {
    const { editButton, label, dataField } = styles
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
        <div className={row}>
          <span className={label}>First name:</span>
          <div className={dataField}>{firstName}</div>
          <span className={label}>Last name:</span>
          <div className={dataField}>{lastName}</div>
        </div>
        <div className={row}>
          <span className={label}>Email address:</span>
          <div className={dataField}>{email}</div>
          <span className={label}>Phone number:</span>
          <div className={dataField}>{phone}</div>
        </div>
        
      </div>
    )
  }
}
