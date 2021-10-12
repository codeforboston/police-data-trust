import * as React from "react"
import styles from "./dashboard-header.module.css"
import Link from "next/link"
import { useRouter } from "next/router"
import { DropdownProps } from "../../models/nav-dropdown"

export default function Nav({ itemProps }: DropdownProps) {
  const router = useRouter()

  const menu = [
    { title: "Search", path: "/search" },
    { title: "Profile", path: "/profile" },
    { title: "Sign Out", path: "/logout" },
    { title: "DONATE", path: "/" } // tbd - external donation page
  ]

  const setClassName = (pathname: string): string => {
    return router.pathname === pathname ? styles.selected : ""
  }

  return (
    <ul id="navMenu">
      {menu.map((item, index) => {
        return (
          <li key={index} className={setClassName(item.path)}>
            <Link href={item.path}>
              <a {...itemProps[index]}>{item.title}</a>
            </Link>
          </li>
        )
      })}
    </ul>
  )
}
