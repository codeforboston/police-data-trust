import styles from './upToDateNotification.module.css'

const UpToDateNotification = () => {
  return (
    <div className={styles.upToDateNotification}>
      <div className={styles.upToDateIcon}/>
      <p>All the resources have been updated to the latest version/dates</p>
    </div>
  )
}

export default UpToDateNotification