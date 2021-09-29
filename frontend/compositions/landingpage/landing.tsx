import React from "react"
import styles from "./landing.module.css"
import { Logo, DonateButton  } from "../../shared-components/" 



export default function LandingPage() {
  return (
  <div>
    <div className={styles.header}>
      <Logo />
    </div>
    <div className = {styles.donate}>
      < DonateButton />
      </div>
      <h1>
        Test
      </h1>
   </div>
  )
}
