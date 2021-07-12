import React, { useState } from "react"
import NPDCLogo from './assets/NPDCLogo.svg'
import LogoMobile from './assets/LogoMobile.svg'
import Banner from './assets/Banner.svg'
import styles  from './header.module.css'
import HamburgerMenu from './assets/Vector.svg'



export default function Header() {
  let [selected, setSelected] = useState('Search');

  const handleNavChange = (e: any) => {
    let value = e.target.innerText;
    setSelected(value);
  }

  const {
    wrapper,
    logoTitle,
    titleContainer,
    mobile,
    desktop,
    nav,
    donate,
  } = styles;

  return (
    <header className={wrapper}>
       <div className={logoTitle}>
          <LogoMobile />
          <div className={titleContainer}>
            <h2 className={mobile}>N.P.D.C.</h2>
            <h2 className={desktop}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>
      <div className={nav}>
        <div className={mobile}>
          <HamburgerMenu />
        </div>
        <button className={donate} type="button">
          <p>DONATE</p>
        </button>
      </div>
    </header>
  )
}


{/* <nav>
          <ul className={nav}>
            <li className={selected === 'Search' ? tab : ''} onClick={handleNavChange}><a href='#'>Search</a></li>
            <li className={selected === 'Profile' ? tab : ''} onClick={handleNavChange}><a href='#'>Profile</a></li>
            <li className={selected === 'About' ? tab : ''} onClick={handleNavChange}><a href='#'>About</a></li>
          </ul>
        </nav> */}