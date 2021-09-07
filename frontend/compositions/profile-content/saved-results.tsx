import * as React from "react"
import styles from "./saved.module.css"
import { UserProfileProps, emptyUser } from "../../models/profile"
import { DataTable } from "../../shared-components/data-table/data-table"

export default function SavedResults({ userData = emptyUser }: UserProfileProps) {
  const [editMode, setEditMode] = React.useState(false)
  const { tableWrapper, tableTitle, editButton } = styles
  return (
    <div className={tableWrapper}>
      <header>
        <span className={tableTitle}>Saved Results</span>
        <button className={editButton}>Edit Results</button>
      </header>
    </div>
  )
}
