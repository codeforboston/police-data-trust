import React, { useState } from "react"
import styles  from './dashboardHeader.module.css'

export default function DesktopNav() {
  let [selected, setSelected] = useState('Search');

  const handleNavChange = (e: React.MouseEvent<Element>) => {
    console.log('link clicked');
    const value = (e.target as HTMLElement).innerText;
    setSelected(value);
  }

  const setClassName = (linkName: string) => {
    if (linkName === selected) {
      return styles.tab;
    }
    return '';
  }

  return (
    <ul className={styles.rightHeader} onClick={handleNavChange}>
      <li className={setClassName('Search')} ><a href='#'>Search</a></li>
      <li className={setClassName('Profile')} ><a href='#'>Profile</a></li>
      <li className={setClassName('About')}><a href='#'>About</a></li>
    </ul>
  )
}



