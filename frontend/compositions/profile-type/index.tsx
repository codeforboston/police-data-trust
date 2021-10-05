import * as React from "react"
import Link from "next/link"
import { profileTypeContent, publicUser, UserDataType } from "../../models/profile"
import { useAuth } from "../../helpers"
import styles from "./profile-type.module.css"

export default function ProfileType() {
  const { user } = useAuth()
  const userData = publicUser(user)
  const { title, content, linkText, linkPath } = profileTypeContent[userData.role]
  const { profileData, sectionTitle, profileTypeText, profileTypeLink, description } = styles
  return (
    <div className={profileData}>
      <header className={sectionTitle}>Your Profile Type</header>
      <div className={profileTypeText}>{title}</div>
      <p className={description}>{content}</p>
      <div className={profileTypeLink}>
        <Link href={linkPath}>
          <a>{linkText}</a>
        </Link>
      </div>
    </div>
  )
}

// can be whoever
export function MockProfileType({ role }: UserDataType) {
  const { title, content, linkText, linkPath } = profileTypeContent[role]
  const { profileData, sectionTitle, profileTypeText, profileTypeLink, description } = styles
  return (
    <div className={profileData}>
      <header className={sectionTitle}>Your Profile Type</header>
      <div className={profileTypeText}>{title}</div>
      <p className={description}>{content}</p>
      <div className={profileTypeLink}>
        <Link href={linkPath}>
          <a>{linkText}</a>
        </Link>
      </div>
    </div>
  )
}
