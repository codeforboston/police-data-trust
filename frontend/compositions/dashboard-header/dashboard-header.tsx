import * as React from "react"
import { Logo as NPDCLogo, PrimaryButton } from "../../shared-components"
import DesktopNav from "./desktop-nav"
import styles from "./dashboard-header.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEllipsisV } from "@fortawesome/free-solid-svg-icons"
import { LogoSizes } from "../../models"
import { useAuth } from "../../helpers"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer } = styles
  const { logout } = useAuth()

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
          <FontAwesomeIcon icon={faEllipsisV} size={"2x"} />
          <DesktopNav />
          <button className="primaryButton" type="button">
            DONATE
          </button>
          <PrimaryButton onClick={logout}>LOGOUT</PrimaryButton>
        </nav>
      </div>
    </header>
  )
}
