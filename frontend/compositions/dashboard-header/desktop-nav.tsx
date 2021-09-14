import * as React from "react"
import styles from "./dashboard-header.module.css"
import Link from "next/link"
import { useRouter } from "next/router"

export default function DesktopNav() {
  const router = useRouter()

  const menu = [
    { title: "Search", path: "/dashboard" },
    { title: "Profile", path: "dashboard/profile" },
    { title: "Sign Out", path: "/test" }
  ]

  const setClassName = (pathname: string): string => {
    return router.pathname === pathname ? styles.tab : ""
  }

  return (
    <ul>
      {menu.map((item, index) => {
        return (
          <li key={index} className={setClassName(item.path)}>
            <Link href={item.path}>
              <a>{item.title}</a>
            </Link>
          </li>
        )
      })}
    </ul>
  )
}
