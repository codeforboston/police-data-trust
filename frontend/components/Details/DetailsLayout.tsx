import React from "react"
import styles from "./detailsLayout.module.css"

interface DetailsLayoutProps {
  children: React.ReactNode
  sidebar?: React.ReactNode
}

export default function DetailsLayout({ children, sidebar }: DetailsLayoutProps) {
  return (
    <div className={styles.detailsBackground}>
      <div className={styles.detailsContainer}>
        <div style={{ maxWidth: "840px", width: "100%" }}>{children}</div>
        <div className={styles.detailsSidebar}>{sidebar}</div>
      </div>
    </div>
  )
}
