import React from "react"
import styles from "./external-link.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons"

interface ExternalLinkProps {
  linkPath: string
  linkText: string
}

export default function ExternalLink({ linkPath, linkText }: ExternalLinkProps) {
  const { externalLink } = styles
  return (
    <a
      aria-label={`${linkText} external`}
      rel="noopener noreferrer"
      target="_blank"
      className={externalLink}
      href={linkPath}>
      {linkText}
      <FontAwesomeIcon aria-hidden="true" icon={faExternalLinkAlt} size="xs" />
    </a>
  )
}
