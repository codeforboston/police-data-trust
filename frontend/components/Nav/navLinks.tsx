"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import styles from "./navLinks.module.css"

interface NavLinkProps {
  text: string
  href: string
  disabled?: boolean
}

interface Props {
  props: NavLinkProps[]
}

export default function NavLinks({ props }: Props) {
  const pathname = usePathname()

  return (
    <div>
      <ul className={styles.links}>
        {props.map((prop) => {
          const isActive = !prop.disabled && pathname === prop.href
          const className = prop.disabled
            ? styles.disabledLink
            : isActive
              ? styles.activeLink
              : styles.inactiveLink

          return (
            <li key={`${prop.text}`} className={className}>
              {prop.disabled ? (
                <span aria-disabled="true">{prop.text}</span>
              ) : (
                <Link href={prop.href}>{prop.text}</Link>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}
