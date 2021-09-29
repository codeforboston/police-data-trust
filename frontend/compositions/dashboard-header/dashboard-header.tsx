import * as React from "react"
import { Logo as NPDCLogo, PrimaryButton } from "../../shared-components"
import Nav from "./nav"
import styles from "./dashboard-header.module.css"
import { LogoSizes } from "../../models"
import { useAuth } from "../../helpers"
import Dropdown from "./dropdown"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer, dropdownTitle } = styles
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
        <nav aria-label="Main Navigation">
          <Dropdown />
          <PrimaryButton>DONATE</PrimaryButton>
          <PrimaryButton onClick={logout}>LOGOUT</PrimaryButton>
        </nav>

      </div>
    </header>
  )
}
