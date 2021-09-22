import * as React from "react"
import { Logo as NPDCLogo, PrimaryButton } from "../../shared-components"
import DesktopNav from "./desktop-nav"
import styles from "./dashboard-header.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faBars } from "@fortawesome/free-solid-svg-icons"
import { LogoSizes } from "../../models"
import { useAuth } from "../../helpers"

export default function DashboardHeader() {
  const {
    wrapper,
    backgroundBanner,
    leftHeader,
    mobileLogo,
    desktopLogo,
    titleContainer,
    mobileTitle,
    desktopTitle
  } = styles
  const { logout } = useAuth()

  return (
    <header className={wrapper}>
      <div className={backgroundBanner}>
        <div className={leftHeader}>
          <div className={mobileLogo}>
            <NPDCLogo size={LogoSizes.SMALL} />
          </div>
          <div className={desktopLogo}>
            <NPDCLogo size={LogoSizes.MEDIUM} />
          </div>
          <div className={titleContainer}>
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>

        <nav>
          <FontAwesomeIcon icon={faBars} size={"2x"} />
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
