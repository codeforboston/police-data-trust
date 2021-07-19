import React from 'react'
import Link from 'next/link'
import styles from './enrollment-cta.module.css'
import { CTATypes, enrollmentCTAText } from '../../models'

interface EnrollmentCTAProps { ctaType: CTATypes }
export default function EnrollmentCTA({ ctaType }: EnrollmentCTAProps) {  
  const { ctaContainer, ctaLink } = styles
  const { description, linkPath, linkText } = enrollmentCTAText[ctaType]

  return (
    <div className={ctaContainer}>
      <p>{description}</p>
      <Link href={linkPath}>
        <a className={ctaLink}>{linkText}</a>
      </Link>
    </div>
  )
}