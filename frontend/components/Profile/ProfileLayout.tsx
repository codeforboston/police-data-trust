import React from "react"
import styles from "./profileLayout.module.css"

interface ProfileLayoutProps {
  children: React.ReactNode
  sidebar?: React.ReactNode
}

export default function ProfileLayout({ children, sidebar }: ProfileLayoutProps) {
  return (
    <div className={styles.profileBackground}>
      <div className={styles.profileContainer}>
        <div style={{ maxWidth: "840px", width: "100%" }}>{children}</div>
        <div className={styles.sidebar}>{sidebar}</div>
      </div>
    </div>
  )
}
