import * as React from "react"
import { useMediaQuery } from './media-query-helper'
import LogoMobile from './assets/LogoMobile.svg'
import NPDCLogo from './assets/NPDCLogo.svg'
import HamburgerMenu from './assets/Vector.svg'
import DesktopNav from './desktopNav'
import styles from './dashboardHeader.module.css'

export default function DashboardHeader() {
  const {
    wrapper,
    backgroundBanner,
    leftHeader,
    logoContainer,
    titleContainer,
    rightHeader,
    nav,
    button,
  } = styles;

  const belowBreakpoint = useMediaQuery(375);
  const logo = belowBreakpoint ? <LogoMobile /> : <NPDCLogo />;
  const title = belowBreakpoint ? 'N.P.D.C.' : 'National Police Data Coalition';
  const navBar = belowBreakpoint ? <HamburgerMenu /> : <DesktopNav />

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          <div className={logoContainer}>
            {logo}
          </div>
          <div className={titleContainer}>
            <h2>{title}</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <div className={rightHeader}>
          <nav className={nav}>
            {navBar}
          </nav>
          <button className={button} type="button">
            <p>DONATE</p>
          </button>
        </div>
      </div>
    </header>
  )
}
