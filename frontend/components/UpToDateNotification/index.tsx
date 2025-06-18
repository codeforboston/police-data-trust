"use client"

import styles from "./upToDateNotification.module.css"

const UpToDateNotification = () => {
  return (
    <div className={styles.wrapper}>
      <div className={styles.upToDateIcon} />
      <p>All the resources have been updated to the latest version/dates</p>
    </div>
  )
}

export default UpToDateNotification
