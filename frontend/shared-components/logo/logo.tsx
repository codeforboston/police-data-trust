import React from "react"
import styles from "./logo.module.css"
import { LogoSizes } from "../../models"
import { logoAlt } from "../../pages/_app"

interface LogoProps {
  size?: LogoSizes
}
export default function Logo({ size = LogoSizes.MEDIUM }: LogoProps) {
  return <img className={`${styles.logo} ${styles[size]}`} src="/NPDCLogo.svg" alt={logoAlt} />
}
