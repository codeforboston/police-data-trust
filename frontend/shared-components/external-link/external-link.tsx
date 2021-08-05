import React from 'react'
import styles from './external-link.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons'

interface ExternalLinkProps { linkPath: string, children: React.ReactNode }

export default function ExternalLink ({ linkPath, children }: ExternalLinkProps) {
  return (
    <a 
      className={styles.externalLink} 
      target="_blank"
      rel="noopener noreferrer"
      href={linkPath}
      >
        {children}
        <FontAwesomeIcon aria-hidden="true" icon={faExternalLinkAlt} size="xs" />
      </a>
  )
}