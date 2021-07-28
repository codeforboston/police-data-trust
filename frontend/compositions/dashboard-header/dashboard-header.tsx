import * as React from "react"
import { Logo as NPDCLogo } from '../../shared-components'
import DesktopNav from "./desktop-nav"
import styles from "./dashboard-header.module.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'

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
    mobileNav,
    desktopNav
  } = styles

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
              <FontAwesomeIcon icon={faBars}/>
            </div>
            <div className={desktopNav}>
              <DesktopNav />
            </div>
          </nav>
          <button className="primaryButton" type="button">
            DONATE
          </button>
        </div>
      </div>
    </header>
  )
}
