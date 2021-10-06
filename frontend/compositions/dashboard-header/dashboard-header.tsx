import * as React from "react"
import { Logo as NPDCLogo, PrimaryButton } from "../../shared-components"
import Nav from "./nav"
import styles from "./dashboard-header.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faEllipsisV } from "@fortawesome/free-solid-svg-icons"
import { LogoSizes } from "../../models"

export default function DashboardHeader() {
  const { wrapper, backgroundBanner, leftHeader, titleContainer, dropdownTitle } = styles

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
          <button
            type="button"
            className={dropdownTitle}
            aria-expanded="false"
            aria-controls="navMenu">
            <FontAwesomeIcon icon={faEllipsisV} size={"3x"} />
          </button>
          <Nav />
          <PrimaryButton>DONATE</PrimaryButton>
        </nav>
      </div>
    </header>
  )
}
