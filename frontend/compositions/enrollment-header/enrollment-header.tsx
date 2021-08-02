import React from "react"
import styles from "./enrollment-header.module.css"
import { InfoTooltip, Logo } from "../../shared-components"
import { TooltipTypes } from "../../models"

interface EnrollmentHeaderProps {
  headerText: string
  tooltip?: TooltipTypes
}
export default function EnrollmentHeader({ headerText, tooltip }: EnrollmentHeaderProps) {
  return (
    <div className={styles.header}>
      <Logo />
      <h1>
        {headerText}
        {tooltip && <InfoTooltip type={tooltip} />}
      </h1>
    </div>
  )
}
