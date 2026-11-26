import type { Metadata } from "next"
import Link from "next/link"
import { ORGANIZATION_DETAILS } from "@/utils/constants"
import DonateButton from "./donateButton"
import styles from "./support.module.css"

export const metadata: Metadata = {
  title: "Support NPDC | National Police Data Coalition",
  description:
    "Support NPDC’s work to make police data easier to find, understand, and use. Donate through PayPal."
}

export default function SupportPage() {
  return (
    <div className={styles.page}>
      <div className={styles.hero}>
        <header className={styles.intro}>
          <p className={styles.eyebrow}>Support our work</p>
          <h1>Support better access to police data</h1>
          <p>
            Police records are scattered across jurisdictions and published in different formats.
            The {ORGANIZATION_DETAILS.name} builds tools to bring that information together, helping
            communities, researchers, advocates, and lawyers understand policing and pursue
            accountability.
          </p>
          <p>Your donation helps support this work.</p>
        </header>

        <section className={styles.donationCard} aria-labelledby="donation-heading">
          <h2 id="donation-heading">Help make this work possible</h2>
          <p>Support NPDC’s work to make police data easier to find, understand, and use.</p>
          <DonateButton />
          <p className={styles.paymentNote}>Complete your donation through PayPal.</p>
        </section>
      </div>

      <section className={styles.impact} aria-labelledby="impact-heading">
        <h2 id="impact-heading">What your support helps us build</h2>
        <div className={styles.impactGrid}>
          <div className={styles.impactCard}>
            <h3>Connected records</h3>
            <p>Bring together police data from different jurisdictions and sources.</p>
          </div>
          <div className={styles.impactCard}>
            <h3>Consistent information</h3>
            <p>Standardize records so they can be searched and understood together.</p>
          </div>
          <div className={styles.impactCard}>
            <h3>Useful tools</h3>
            <p>
              Develop and maintain infrastructure that supports research, transparency, and public
              accountability.
            </p>
          </div>
        </div>
      </section>

      <section className={styles.organization} aria-labelledby="organization-heading">
        <div className={styles.organizationDetails}>
          <h2 id="organization-heading">{ORGANIZATION_DETAILS.name}</h2>
          <p>Registered nonprofit · EIN: {ORGANIZATION_DETAILS.ein}</p>
          <div className={styles.links}>
            <Link className={styles.link} href="/about">
              Learn about NPDC
            </Link>
            <Link className={styles.link} href="/contact">
              Contact us
            </Link>
          </div>
        </div>
        <a
          className={styles.candidSeal}
          aria-label="National Police Data Coalition on Candid (opens in a new tab)"
          href="https://app.candid.org/profile/14056587/national-police-data-coalition-87-4427926/?pkId=0c108ba0-7918-4665-808d-4d00b6d77c09"
          target="_blank"
          rel="noopener noreferrer"
        >
          {/* Load Candid’s live seal directly so its status stays current. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            alt=""
            src="https://widgets.guidestar.org/prod/v1/pdp/transparency-seal/14056587/svg"
            width={150}
            height={150}
            loading="lazy"
          />
        </a>
      </section>
    </div>
  )
}
