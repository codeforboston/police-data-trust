import Link from "next/link"
import { ORGANIZATION_DETAILS } from "@/utils/constants"
import styles from "./footer.module.css"

export default function Footer() {
  const { address } = ORGANIZATION_DETAILS

  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <section className={styles.section} aria-label="Organization details">
          <p className={styles.name}>{ORGANIZATION_DETAILS.name}</p>
        </section>

        <section className={styles.section} aria-label="Contact details">
          <p className={styles.label}>Contact</p>
          <p className={styles.text}>
            {address.street}
            <br />
            {address.suite && (
              <>
                {address.suite}
                <br />
              </>
            )}
            {address.cityStateZip}
          </p>
          <a className={styles.link} href={`mailto:${ORGANIZATION_DETAILS.email}`}>
            {ORGANIZATION_DETAILS.email}
          </a>
        </section>

        <nav className={styles.section} aria-label="Footer navigation">
          <p className={styles.label}>Pages</p>
          <div className={styles.links}>
            <Link className={styles.link} href="/about">
              About
            </Link>
            <Link className={styles.link} href="/contact">
              Contact
            </Link>
            <Link className={styles.link} href="/search">
              Search
            </Link>
            <Link className={styles.link} href="/overview">
              Overview
            </Link>
          </div>
        </nav>
      </div>
    </footer>
  )
}
