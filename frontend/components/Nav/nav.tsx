"use client"

import Image from "next/image"
import Link from "next/link"
import Chip from "@mui/material/Chip"
import Logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import NavLinks from "./navLinks"
import NavIcons from "./navIcons"
import styles from "./nav.module.css"

export default function Nav() {
  const Links = [
    { text: "Home", href: "/" },
    { text: "Data Explorer", href: "/data-explorer", disabled: true },
    { text: "Community", href: "/community", disabled: true },
    { text: "Collection", href: "/collection", disabled: true }
  ]
  return (
    <nav className={styles.nav}>
      <div>
        <div className={styles.navHeader}>
          <Link
            href="https://form.typeform.com/to/EqrXBz3Q"
            className={styles.feedback}
            target="_blank"
            rel="noreferrer"
          >
            {" "}
            Feedback
          </Link>
        </div>
        <div className={styles.navLower}>
          <Link href="/" className={styles.dashHeader}>
            <Image src={Logo} alt="Logo" width={52} height={52} />
            <div className={styles.logoTxt}>
              <p className={styles.title}>National Police Data Coalition</p>
              <p>The national index of police incidents </p>
            </div>
            <Chip
              label="Beta"
              size="small"
              className={styles.betaChip}
              sx={{
                backgroundColor: "#7E328B",
                color: "#fff",
                fontWeight: 700
              }}
            />
          </Link>
          <NavLinks props={Links} />
          <NavIcons />
        </div>
      </div>
    </nav>
  )
}
