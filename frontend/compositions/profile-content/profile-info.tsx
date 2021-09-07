import * as React from "react"
import styles from "./profile-content.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEdit } from "@fortawesome/free-solid-svg-icons"
import { UserProfileProps, emptyUser } from "../../models/profile"

export default function ProfileInfo({ userData = emptyUser }: UserProfileProps) {
  const [editMode, setEditMode] = React.useState(false)
  const { profileData, sectionTitle, row } = styles
  const { firstName, lastName, email, phone } = userData

  function handleSubmit(e: React.FormEvent) {
    // TODO: update user
  }

  if (editMode) {
    return (
      <div className={profileData}>
        <header className={sectionTitle}>Edit Your Account Information</header>
        <form onSubmit={handleSubmit}>
          <div className={row}>
            <label htmlFor="firstName">First name:</label>
            <input type="text" id="firstName" placeholder={firstName} />
            <label htmlFor="lastName">Last name:</label>
            <input type="text" id="lastName" placeholder={lastName} />
          </div>
          <div className={row}>
            <label htmlFor="email">Email address:</label>
            <input type="email" id="email" placeholder={email} />
            <label htmlFor="phone">Phone number:</label>
            <input type="phone" id="phone" placeholder={phone} />
          </div>
          <div className={row}>
            <label htmlFor="newPassword">Password:</label>
            <input type="password" id="newPassword" />
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <input type="password" id="confirmPassword" />
          </div>
          <div className={row}>
            <button className={styles.cancelButton} onClick={() => setEditMode(false)}>
              Cancel
            </button>
            <input type="submit" className={styles.submitButton} value="Save Changes" />
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
        <div className={row}>
          <span className={label}>Password:</span>
          <div className={dataField}>********</div>
        </div>
      </div>
    )
  }
}
