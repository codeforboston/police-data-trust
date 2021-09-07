import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/router"
import styles from "./dashboard-header.module.css"
import { headerTabs } from "../../models/header-nav"

export default function DesktopNav() {
  const router = useRouter()

  const clsName = (loc: string): string => {
    return loc === router.pathname ? styles.tab : ""
  }

  return (
    <nav>
      <ul className={styles.rightHeader}>
        {headerTabs.map((tab) => (
          <li key={tab.loc} className={clsName(tab.loc)}>
            <Link href={tab.loc}>{tab.text}</Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
