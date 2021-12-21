import React from "react"
import { Logo } from ".."
import { LogoSizes } from "../../models"
import styles from "./success-page.module.css"

interface SuccessPageProps {
  message: string
}

export default function SuccessPage({ message }: SuccessPageProps) {

  return (
    <div className={styles.center}>
      <Logo size={LogoSizes.LARGE}/>
      <div className={styles.text}>
        <h1>Success!</h1>
        <p>{message}</p>
        <a href="/">Return Home</a>
      </div>
    </div>
  )
}