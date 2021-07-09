import React, { useState } from "react"
import NPDCLogo from './assets/NPDCLogo.svg'
import styles  from './header.module.css'



export default function Header() {
  let [selected, setSelected] = useState('Search');

  const handleNavChange = (e: any) => {
    let value = e.target.innerText;
    setSelected(value);
  }

  const { wrapper, banner, logoTitle, titleContainer, nav, tab, donate, navDonate} = styles;

  return (
    <header className={wrapper}>
      <div className={banner}>
        <div className={logoTitle}>
          <NPDCLogo />
          <div className={titleContainer}>
            <h2>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>
        <div className={navDonate}>
          <nav>
            <ul className={nav}>
              <li className={selected === 'Search' ? tab : ''} onClick={handleNavChange}>Search</li>
              <li className={selected === 'Profile' ? tab : ''} onClick={handleNavChange}>Profile</li>
              <li className={selected === 'About' ? tab : ''} onClick={handleNavChange}>About</li>
            </ul>
          </nav>
          <button className={donate}type="button">DONATE</button>
        </div>
      </div>
    </header>
  )
}
