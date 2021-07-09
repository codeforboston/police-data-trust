import React, { useState } from "react"
import NPDCLogo from './assets/NPDCLogo.svg'
import styles  from './header.module.css'



export default function Header() {
  let [selected, setSelected] = useState('Search');

  const handleNavChange = (e: any) => {
    let value = e.target.innerText;
    setSelected(value);
  }

  const { wrapper, banner, logo, titleContainer, title, subtitle, nav, tab, donate } = styles;

  return (
    <header className={wrapper}>
      <div className={banner}>
        <div className={logo}>
          <NPDCLogo />
        </div>
        <div className={titleContainer}>
          <h2 className={title}>National Police Data Coalition</h2>
          <p className={subtitle}>The national index of police incidents</p>
        </div>
        <nav>
          <ul className={nav}>
            <li className={selected === 'Search' ? tab : ''} onClick={handleNavChange}>Search</li>
            <li className={selected === 'Profile' ? tab : ''} onClick={handleNavChange}>Profile</li>
            <li className={selected === 'About' ? tab : ''} onClick={handleNavChange}>About</li>
          </ul>
        </nav>
        <div className={donate}>
          <button type="button">DONATE</button>
        </div>
      </div>
    </header>
  )
}
