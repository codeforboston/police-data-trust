import * as React from 'react'
import styles from './saved.module.css'
import { UserProfileProps, emptyUser } from '../../models/profile'


// placeholders
export default function SavedSearches({ userData = emptyUser }: UserProfileProps) {
  const [editMode, setEditMode] = React.useState(false)
  const { tableWrapper, tableTitle, editButton } = styles
  return (
    <div className={tableWrapper} >
      <header >
        <span className={tableTitle}>Saved Searches</span>
        <button className={editButton}>Edit Searches</button>
      </header>

     
    </div>
    
    )
}