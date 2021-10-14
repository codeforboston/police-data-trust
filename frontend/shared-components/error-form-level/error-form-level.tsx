import React from "react"
import styles from "./error-form-level.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faExclamationCircle } from "@fortawesome/free-solid-svg-icons"

interface FormLevelErrorProps {
  errorId: string
  errorMessage: string
}
export default function FormLevelError({ errorId, errorMessage }: FormLevelErrorProps) {
  return (
    <p id={errorId} className={styles.error} role="alert">
      <FontAwesomeIcon aria-hidden="true" icon={faExclamationCircle} />
      &nbsp;{errorMessage}
    </p>
  )
}
