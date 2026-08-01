import { ORGANIZATION_DETAILS } from "@/utils/constants"
import styles from "./about.module.css"

export default function AboutPage() {
  const { address } = ORGANIZATION_DETAILS

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <p className={styles.eyebrow}>Registered nonprofit</p>
        <h1 className={styles.title}>{ORGANIZATION_DETAILS.name}</h1>
        <p className={styles.mission}>{ORGANIZATION_DETAILS.mission}</p>
      </header>

      <section className={styles.details} aria-label="Nonprofit verification details">
        <div className={styles.detail}>
          <p className={styles.label}>Registered name</p>
          <p className={styles.value}>{ORGANIZATION_DETAILS.name}</p>
        </div>
        <div className={styles.detail}>
          <p className={styles.label}>EIN</p>
          <p className={styles.value}>{ORGANIZATION_DETAILS.ein}</p>
        </div>
        <div className={styles.detail}>
          <p className={styles.label}>Mailing Address</p>
          <p className={styles.value}>
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
        </div>
      </section>

      <section className={styles.section}>
        <h2>What We Do</h2>
        <p>
          NPDC builds infrastructure for aggregating, standardizing, and sharing police data across
          jurisdictions. Our work supports transparency, public accountability, and better access to
          records for advocates, agencies, lawyers, policy makers, and communities.
        </p>
      </section>

      <section className={styles.section}>
        <h2>Contact</h2>
        <p>
          Reach us at{" "}
          <a className={styles.link} href={`mailto:${ORGANIZATION_DETAILS.email}`}>
            {ORGANIZATION_DETAILS.email}
          </a>
          .
        </p>
      </section>
    </div>
  )
}
