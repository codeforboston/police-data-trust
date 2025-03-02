'use client'

import Link from "next/link";
import styles from "./mobileNav.module.css";

export default function MobileNav() {

      return (
        <div className={styles.mobileNav}>
            <ul className={styles.ul}>
                <li className={styles.li}>  
                    <Link href="/1">Home</Link>
                </li>
                <li className={styles.li}>  
                    <Link href="/2">Data Explore</Link>
                </li>
                <li className={styles.li}>  
                    <Link href="/3">Create</Link>
                </li>
                <li className={styles.li}>  
                    <Link href="/4">Community</Link>
                </li>
                <li className={styles.li}>  
                    <Link href="/5">Collection</Link>
                </li>
            </ul>
        </div>
      )
}