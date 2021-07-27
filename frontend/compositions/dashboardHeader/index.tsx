import * as React from "react"
import HamburgerMenu from "../../public/Vector.svg"
import DesktopNav from "./desktopNav"
import styles from "./dashboardHeader.module.css"
import { Logo as NPDCLogo } from "../index"

export default function DashboardHeader() {
  const {
    wrapper,
    backgroundBanner,
    leftHeader,
    titleContainer,
    mobileTitle,
    desktopTitle,
  } = styles

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          <NPDCLogo />
          <div className={titleContainer}>
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <nav>
          <HamburgerMenu />
          <DesktopNav />
          <button
            className="primaryButton"
            type="button">
             DONATE
          </button>
        </nav>
      </div>
    </header>
  )
}
