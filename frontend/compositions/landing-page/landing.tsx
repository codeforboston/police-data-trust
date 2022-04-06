import React from "react"
import { useRouter } from "next/router"
import styles from "./landing.module.css"
import { Logo, PrimaryButton } from "../../shared-components"
import { AppRoutes } from "../../models"
export default function LandingPage() {
  const router = useRouter()
  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <Logo />
        <button
          className="primaryButton"
          style={{
            backgroundColor: "white",
            color: "#303463",
            border: "#303463 thin solid",
            fontWeight: "bold",
            margin: "2rem 2rem 0 0"
          }}>
          Donate
        </button>
      </div>
      <div className={styles.content}>
        <h1 className={styles.title}>Data to keep our communities safer</h1>
        <p className={styles.text}>Police brutality thrives in anonymity.</p>
        <p className={styles.text}>
          For too long, records of police violence have been obscure, inacessible, and incomplete.
        </p>
        <p className={styles.emphasis}>We&apos;re Changing That.</p>
      </div>
      <PrimaryButton onClick={() => router.push(AppRoutes.REGISTER)}>Join Us</PrimaryButton>
      <a href="#">Learn More</a>
    </div>
  )
}
