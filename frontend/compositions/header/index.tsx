import React, { useState } from "react"
import NPDCLogo from './assets/NPDCLogo.svg'
import styles from './header.module.css'


export default function Header() {
  let [selected, setSelected] = useState('Search');

  const handleNavChange = (e: any) => {
    let value = e.target.innerText;
    setSelected(value);
  }

  return (
    <header className={styles.container}>
      <div className={styles.banner}>
        <div className={styles.logo}>
          <NPDCLogo />
        </div>
        <div className={styles.titleContainer}>
          <h2 className={styles.title}>National Police Data Coalition</h2>
          <p className={styles.subtitle}>The national index of police incidents</p>
        </div>
        <nav>
          <ul className={styles.nav}>
            <li className={selected === 'Search' ? styles.tab : ''} onClick={handleNavChange}>Search</li>
            <li className={selected === 'Profile' ? styles.tab : ''} onClick={handleNavChange}>Profile</li>
            <li className={selected === 'About' ? styles.tab : ''} onClick={handleNavChange}>About</li>
          </ul>
        </nav>
        <div className={styles.item4}>
          Grid Item 4
        </div>
      </div>
    </header>
  )
}
