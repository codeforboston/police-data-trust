import React from "react"
import styles from "./enrollment-header.module.css"
import { InfoTooltip } from "../../shared-components/index"
import { TooltipTypes } from "../../models"
import { Logo } from ".."

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
