import * as React from "react"
import useDropdownMenu from "react-accessible-dropdown-menu-hook"
import { useMediaQuery } from "react-responsive"
import { AuthContext } from "../../helpers/auth"
import { LogoSizes } from "../../models"
import { Logo as NPDCLogo } from "../../shared-components"
import styles from "./dashboard-header.module.css"
import MobileDropdown from "./mobile-dropdown"
import Nav from "./nav"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer } = styles
  const { buttonProps, itemProps, isOpen } = useDropdownMenu(4)
  const desktop = useMediaQuery({ query: "screen and (min-width: 32em)" })

  const { user } = React.useContext(AuthContext)

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
        {/* Only show the buttons if the user is logged in */}
        {user && (
          <nav aria-label="Main Navigation">
            {desktop ? (
              <Nav itemProps={itemProps} />
            ) : (
              <MobileDropdown itemProps={itemProps} buttonProps={buttonProps} isOpen={isOpen} />
            )}
          </nav>
        )}
      </div>
    </header>
  )
}
