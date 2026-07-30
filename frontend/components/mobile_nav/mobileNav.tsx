"use client"

import Link from "next/link"
import styles from "./mobileNav.module.css"
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined"
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined"
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined"
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined"
import MailOutlineOutlinedIcon from "@mui/icons-material/MailOutlineOutlined"
import { usePathname } from "next/navigation"

export default function MobileNav() {
  const pathname = usePathname()

  return (
    <div className={styles.mobileNav}>
      <ul className={styles.ul}>
        <li className={pathname === "/" ? `${styles.active}` : styles.li}>
          <HomeOutlinedIcon className={styles.icon} />
          <Link href="/">Home</Link>
        </li>
        <li className={pathname === "/search" ? `${styles.active}` : styles.li}>
          <SearchOutlinedIcon className={styles.icon} />
          <Link href="/search">Search</Link>
        </li>
        <li className={pathname === "/overview" ? `${styles.active}` : styles.li}>
          <TimelineOutlinedIcon className={styles.icon} />
          <Link href="/overview">Overview</Link>
        </li>
        <li className={pathname === "/about" ? `${styles.active}` : styles.li}>
          <InfoOutlinedIcon className={styles.icon} />
          <Link href="/about">About</Link>
        </li>
        <li className={pathname === "/contact" ? `${styles.active}` : styles.li}>
          <MailOutlineOutlinedIcon className={styles.icon} />
          <Link href="/contact">Contact</Link>
        </li>
      </ul>
    </div>
  )
}
