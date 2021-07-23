import * as React from "react"
import NPDCLogo from '../../shared-components/logo'
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
    mobileTitle,
    desktopTitle,
    rightHeader,
    nav,
    buttonContainer,
    mobileNav,
    desktopNav,
  } = styles;

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          <div className={logoContainer}>
            <NPDCLogo />
          </div>
          <div className={titleContainer}>
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <div className={rightHeader}>
          <nav className={nav}>
            <div className={mobileNav}>
              <HamburgerMenu />
            </div>
            <div className={desktopNav}>
              <DesktopNav />
            </div>
          </nav>
          <div className={buttonContainer}>
            <button className="primaryButton" type="button">
              DONATE
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
