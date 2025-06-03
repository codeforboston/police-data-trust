'use client'

import Image from "next/image";
import Link from "next/link";
import Logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import NavLinks from "./navLinks";
import NavIcons from "./navIcons";
import styles from "./nav.module.css";

export default function Nav() {

  const Links = [
    { text: "Home", href: "/" },
    { text: "Data Explorer", href: "/data-explorer" },
    { text: "Community", href: "/community" },
    { text: "Collection", href: "/collection" },
  ];
  return (
    <nav className= {styles.nav} >
      <div>
        <div className={styles.navHeader}>
          <Link href="/feedback" className={styles.feedback}> Feedback</Link>
        </div>
        <div className={styles.navLower}>
          <div className={styles.dashHeader}>
            <Image src={Logo} alt="Logo" width={44} height={44} />
            <div className={styles.logoTxt}>
              <p className={styles.title} >National Police Data Coalition</p>
              <p>The national index of police incidents </p>
            </div>
          </div>
          <NavLinks props={Links} />
          <NavIcons />
        </div>
      </div>
    </nav>
  );
}