import React from "react"
import styles from "./results-alert.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons"
import { alertContent, SearchResultsTypes } from "../../models"
import { PrimaryButton } from "../"

interface ResultsAlertProps {
  type: SearchResultsTypes
  returnHandler(): any
}

export default function ResultsAlert({ type, returnHandler }: ResultsAlertProps) {
  const alertMessage = alertContent[type]
  return (
    <div className={styles.outerBox} role="alert">
      <div className={styles.innerBox}>
        <FontAwesomeIcon size="2x" icon={faExclamationTriangle} />
        <div>
          <span className={styles.alertMessage}>{alertMessage}</span>
          <p>Please revise search or explore map</p>
        </div>
      </div>

      <PrimaryButton onClick={returnHandler}>Return</PrimaryButton>
    </div>
  )
}
