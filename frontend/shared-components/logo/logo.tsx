import React from "react"
import styles from './logo.module.css'
import { logoAlt } from '../../pages/_app'

interface LogoProps { size?: string }

export default function Logo({ size = 'medium' }: LogoProps) {
  return (
    <img 
      className={`${styles.logo} ${styles[size]}`} 
      src="/NPDCLogo.svg" 
      alt={logoAlt} 
    />
  )
}
