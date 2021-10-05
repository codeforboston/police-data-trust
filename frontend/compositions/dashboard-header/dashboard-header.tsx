import * as React from "react"
import useDropdownMenu from "react-accessible-dropdown-menu-hook"
import { Logo as NPDCLogo, PrimaryButton } from "../../shared-components"
import Nav from "./nav"
import styles from "./dashboard-header.module.css"
import { LogoSizes } from "../../models"
import { useAuth } from "../../helpers"
import MobileDropdown from "./mobile-dropdown"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer } = styles
  const { buttonProps, itemProps, isOpen } = useDropdownMenu(4)
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
          <MobileDropdown itemProps={itemProps} buttonProps={buttonProps} isOpen={isOpen} />
          <Nav itemProps={itemProps} />
          <PrimaryButton>DONATE</PrimaryButton>
          <PrimaryButton onClick={logout}>LOGOUT</PrimaryButton>
        </nav>
      </div>
    </header>
  )
}
