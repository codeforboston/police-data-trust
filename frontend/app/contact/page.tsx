import { ORGANIZATION_DETAILS } from "@/utils/constants"
import styles from "./contact.module.css"

export default function ContactPage() {
  const { address } = ORGANIZATION_DETAILS

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Contact {ORGANIZATION_DETAILS.abbreviation}</h1>
      <p className={styles.intro}>
        For partnership, data access, grant verification, and general questions, contact the
        National Police Data Coalition using the details below.
      </p>

      <section className={styles.details} aria-label="Contact and nonprofit details">
        <div className={styles.detail}>
          <p className={styles.label}>Email</p>
          <a className={styles.link} href={`mailto:${ORGANIZATION_DETAILS.email}`}>
            {ORGANIZATION_DETAILS.email}
          </a>
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
        <div className={styles.detail}>
          <p className={styles.label}>Registered nonprofit name</p>
          <p className={styles.value}>{ORGANIZATION_DETAILS.name}</p>
        </div>
        <div className={styles.detail}>
          <p className={styles.label}>EIN</p>
          <p className={styles.value}>{ORGANIZATION_DETAILS.ein}</p>
        </div>
      </section>
    </div>
  )
}
