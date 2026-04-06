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
        <div className={sidebar ? styles.detailsMainWithSidebar : styles.detailsMain}>
          {children}
        </div>
        {sidebar && <div className={styles.detailsSidebar}>{sidebar}</div>}
      </div>
    </div>
  )
}
