import React from "react"
import Link from "next/link"
import styles from "./enrollment-call-to-action.module.css"
import { CallToActionTypes, enrollmentCallToActionText } from "../../models"

interface EnrollmentCallToActionProps {
  callToActionType: CallToActionTypes
}
export default function EnrollmentCallToAction({ callToActionType }: EnrollmentCallToActionProps) {
  const { callToActionContainer, callToActionLink } = styles
  const { description, linkPath, linkText } = enrollmentCallToActionText[callToActionType]

  return (
    <div className={callToActionContainer}>
      <p>{description}</p>
      <Link href={linkPath}>
        <a className={callToActionLink}>{linkText}</a>
      </Link>
    </div>
  )
}
