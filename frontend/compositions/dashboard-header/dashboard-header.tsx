import * as React from "react"
import useDropdownMenu from "react-accessible-dropdown-menu-hook"
import { useMediaQuery } from "react-responsive"
import { LogoSizes } from "../../models"
import { Logo as NPDCLogo } from "../../shared-components"
import styles from "./dashboard-header.module.css"
import MobileDropdown from "./mobile-dropdown"
import Nav from "./nav"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer } = styles
  const { buttonProps, itemProps, isOpen } = useDropdownMenu(4)
  const mobile = useMediaQuery({ query: "screen and (max-width: 32em)" })

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
          {mobile ? (
            <MobileDropdown itemProps={itemProps} buttonProps={buttonProps} isOpen={isOpen} />
          ) : (
            <Nav itemProps={itemProps} />
          )}
        </nav>
      </div>
    </header>
  )
}
