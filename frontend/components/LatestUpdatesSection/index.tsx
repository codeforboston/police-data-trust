"use client"

import styles from "./latestUpdateSection.module.css"
import UpdateCard from "./UpdateCard"

const LatestUpdates = () => {
  return (
    <section className={styles.latestUpdatesWrapper}>
      <h2 className={styles.latestUpdatesHeading}>Latest Updates</h2>
      <ul className={styles.cardSection}>
        <UpdateCard title="Incident" updates={["New add one", "New add one", "New add one"]} />
        <UpdateCard title="Post" updates={["New add one", "New add one", "New add one"]} />
        <UpdateCard title="Following" updates={["New add one", "New add one", "New add one"]} />
      </ul>
    </section>
  )
}

export default LatestUpdates
