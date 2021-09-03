import * as React from 'react'
import styles from './profile-content.module.css'
import { UserProfileProps, emptyUser } from '../../models/profile'
import ProfileInfo from './profile-info'
import ProfileType from './profile-type'


// placeholders
const SavedSearch = ({ userData = emptyUser }: UserProfileProps) => {

  return (
    <div className={styles.savedData}>
      <header className={styles.dataTitle}>
        Saved Searches
        <button>Edit Searches</button>
      </header>
    </div>
    
    )
}

const SavedResults = ({ userData = emptyUser }: UserProfileProps) => {
  return (
    <div className={styles.savedData}>
      <header className={styles.dataTitle}>
        Saved Results
        <button>Edit Results</button>
      </header>
    </div>
    
    )
}


export {
  ProfileInfo,
  ProfileType,
  SavedResults,
  SavedSearch
}