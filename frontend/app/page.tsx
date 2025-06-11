"use client"
import styles from "./page.module.css"
import { useAuth } from "@/context/AuthProvider"

export default function Home() {
  const { isLoggedIn } = useAuth()
  return (
    <div className={styles.page}>
      <h1>This is the Home Page!</h1>
      <p className={styles.txt}> More to come soon!</p>
      <p className={styles.txt}>{isLoggedIn ? "You are logged in!" : "You are not logged in."}</p>
    </div>
  )
}
