import React from "react"
import styles from "./landing.module.css"
import { Logo, PrimaryButton } from "../../shared-components/" 



export default function LandingPage() {
  return (
  <div>
    <div className={styles.header}>
      <Logo />
      
      <PrimaryButton style={{backgroundColor: "white", color: "#303463", border: "#303463 thin solid"    }}>Donate</PrimaryButton>
    </div>
      <div className={styles.text}>
      <h1>
        Data to keep our communities safer
      </h1>
      <div>
      Police brutality thrives in anonymity. 
      </div>
      <div>
      For too long, records of police violence have been obscure, inacessible, and incomplete. 
      </div>
      <div>
      We're Changing That. 
      </div>
      </div>
      <PrimaryButton>Join Us</PrimaryButton>
     

   </div>
  )
}
