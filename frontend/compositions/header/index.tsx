import React from "react"
import NPDCLogo from './assets/NPDCLogo.svg'
import styles from './header.module.css'

export default function Header() {
  return (
    <div className={styles.container}>
      <div className={styles.logo}>
        <NPDCLogo />
      </div>
      <div className={styles.titleContainer}>
          <h2>National Police Data Coalition</h2>
          <p className={styles.subtitle}>The national index of police incidents</p>
      </div>
      <div className={styles.links}>
        <button className={styles.search}>Search</button>
        <button>My Profile</button>
        <button>About Us</button>
      </div>
    </div>
  )
}