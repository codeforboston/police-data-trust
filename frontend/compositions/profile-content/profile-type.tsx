import * as React from 'react'
import Link from 'next/link'
import styles from './profile-content.module.css'
import { UserProfileProps, profileTypeContent, emptyUser } from '../../models/profile'


export default function ProfileType({ userData = emptyUser }: UserProfileProps) {
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