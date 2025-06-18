"use client"
import styles from "./page.module.css"
import SearchBar from "@/components/SearchBar"
import LatestUpdates from "@/components/LatestUpdatesSection"
import UpToDateNotification from "@/components/UpToDateNotification"

export default function Home() {
  return (
    <div className={styles.page}>
      <h1 className={styles.heading}>How can we help you?</h1>
      <SearchBar />
      <LatestUpdates />
      <UpToDateNotification />
    </div>
  )
}
