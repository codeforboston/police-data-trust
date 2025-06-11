"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import styles from "./navLinks.module.css"

interface NavLinkProps {
  text: string
  href: string
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
          const isActive = pathname === prop.href
          return (
            <li
              key={`${prop.text}`}
              className={isActive ? `${styles.activeLink}` : `${styles.inactiveLink}`}
            >
              <Link href={prop.href}>{prop.text}</Link>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
