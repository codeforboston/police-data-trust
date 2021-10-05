import * as React from "react"
import styles from "./view-info.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEdit } from "@fortawesome/free-solid-svg-icons"
import { useAuth } from "../../helpers"
import EditProfileInfo from "../profile-edit"
import { publicUser } from "../../models/profile"

export default function ProfileInfo() {
  const [editMode, setEditMode] = React.useState(false)

  const { profileData, sectionTitle } = styles
  const { user } = useAuth()
  // temp
  const userData = publicUser(user)
  const { firstName, lastName, email, phone } = userData

  if (editMode) {
    return <EditProfileInfo cancelEditMode={() => setEditMode(false)} />
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
