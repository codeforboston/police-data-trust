import * as React from 'react'
import Link from 'next/link'
import styles from './profile-content.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEdit } from "@fortawesome/free-solid-svg-icons"
import { UserType, profileTypeContent, emptyUser } from '../../models/profile'

interface UserProfileProps {
  userData: UserType
}


export function ProfileInfo({ userData = emptyUser }: UserProfileProps) {
  const [editMode, setEditMode] = React.useState(false)
  const { profileData, sectionTitle, row } = styles

  function handleSubmit(e: React.FormEvent) {
    console.log('edit profile form submitted')
  }

  if (editMode) {
    return (
      <div className={profileData}>
        <header className={sectionTitle}>Edit Your Account Information</header>
        <form onSubmit={handleSubmit} >
          <div className={row}>
            <label htmlFor="firstName">First name:</label>
            <input type="text" id="firstName" placeholder={userData.firstName} />
            <label htmlFor="lastName">Last name:</label>
            <input type="text" id="lastName" placeholder={userData.lastName} />
          </div>
          <div className={row}>
            <label htmlFor="email">Email address:</label>
            <input type="email" id="email" placeholder={userData.email} />
            <label htmlFor="phone">Phone number:</label>
            <input type="phone" id="phone" placeholder={userData.phone} />
          </div>
          <div className={row}>
            <label htmlFor="newPassword">Password:</label>
            <input type="password" id="newPassword" />
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <input type="password" id="confirmPassword" />
          </div>
          <div className={row}>
            <button onClick={() => setEditMode(false)}>Cancel</button>
            <input type="submit" value="Save Changes" />
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
            onClick={() => setEditMode(true)} />
        </header>
        <div className={row}>
          <span className={label}>First name:</span>
          <div className={dataField}>{userData.firstName}</div>
          <span className={label}>Last name:</span>
          <div className={dataField}>{userData.lastName}</div>
        </div>
        <div className={row}>
          <span className={label}>Email address:</span>
          <div className={dataField}>{userData.email}</div>
          <span className={label}>Phone number:</span>
          <div className={dataField}>{userData.phone}</div>
        </div>
        <div className={row}>
          <span className={label}>Password:</span>
          <div className={dataField}>********</div>
        </div>
        
      </div>
    )
  }
  
}

export const ProfileType = ({ userData = emptyUser }: UserProfileProps) => {
  const {title, content, linkText, linkPath } = profileTypeContent[userData.role]
  const { profileData, sectionTitle, profileTypeText, profileTypeLink, description } = styles
  return (
    <div className={profileData}>
      <header className={sectionTitle}>Your Profile Type</header>
      <div className={profileTypeText}>{title}</div>
      <p className={description}>{content}</p>
      <div className={profileTypeLink}>
        <Link href={linkPath}>{linkText}</Link>
      </div>
    </div>
  )
}


// placeholders
export const SavedSearch = ({ userData = emptyUser }: UserProfileProps) => {

  return (
    <div className={styles.profileData}>
      <header className={styles.sectionTitle}>Saved Searches</header>
    </div>
    
    )
}

export const SavedResults = ({ userData = emptyUser }: UserProfileProps) => {
  return (
    <div className={styles.profileData}>
      <header className={styles.sectionTitle}>Saved Results</header>
    </div>
    
    )
}
