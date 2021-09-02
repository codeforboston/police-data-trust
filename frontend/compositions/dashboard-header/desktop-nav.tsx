import * as React from "react"
import Link from "next/link"
import styles from "./dashboard-header.module.css"
import { AppRoutes } from "../../models"


interface NavTypes {
  loc: AppRoutes,
  text: string
}

const topNav: NavTypes[] = [
  { loc: AppRoutes.DASHBOARD, text: 'Search' },
  { loc: AppRoutes.PROFILE, text: 'Profile' },
  { loc: AppRoutes.ABOUT, text: 'About' }
]

interface DesktopNavProps {
  currentNav: string,
  selectNav: Function
}

export default function DesktopNav({ currentNav, selectNav}: DesktopNavProps) {


  const clsName = (loc: string): string => {
    return loc === currentNav ? styles.tab : ""
  }

  return (
    <ul className={styles.rightHeader}>
      {topNav.map(itm => (
        <li key={itm.loc} className={clsName(itm.loc)} onClick={() => selectNav(itm.loc)}>
          <Link href={itm.loc}>
            <a>{itm.text}</a>
          </Link>
        </li>
      ))}
    </ul>
  )
}
