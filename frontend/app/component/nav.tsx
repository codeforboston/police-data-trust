'use server'

import Image from "next/image";
import Link from "next/link";
import Logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import styles from "./nav.module.css";

export default async function Nav() {
  return (
    <nav className= {styles.nav} >
      <div className={styles.navHeader}>
        <Link href="/feedback" className={styles.feedback}> Feedback</Link>      </div>
      <div>
        <div className={styles.dashHeader}>
          <Image src={Logo} alt="Logo" width={44} height={44} />
          <div className={styles.logoTxt}>
            <p className={styles.title} >National Police Data Coalition</p>
            <p>The national index of police incidents </p>
          </div>
        </div>
      </div>
    </nav>
  );
}