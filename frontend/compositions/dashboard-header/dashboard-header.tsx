import * as React from "react"
import { Logo as NPDCLogo } from "../../shared-components"
import DesktopNav from "./desktop-nav"
import styles from "./dashboard-header.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faBars } from "@fortawesome/free-solid-svg-icons"
import { LogoSizes } from "../../models"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer } = styles

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          <NPDCLogo size={LogoSizes.MEDIUM} />
          <div className={titleContainer}>
            <h2>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <nav>
          <FontAwesomeIcon icon={faBars} size={"2x"} />
          <DesktopNav />
          <button className="primaryButton" type="button">
            DONATE
          </button>
        </nav>
      </div>
    </header>
  )
}
