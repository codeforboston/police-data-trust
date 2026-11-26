"use client"

import Script from "next/script"
import { useRef, useState } from "react"
import styles from "./support.module.css"

const HOSTED_BUTTON_ID = "KWDM4H3KATHA2"

type DonationOptions = {
  env: "production"
  hosted_button_id: string
  image: { src: string; alt: string; title: string }
}

declare global {
  interface Window {
    PayPal?: {
      Donation: {
        Button: (options: DonationOptions) => { render: (selector: string) => void }
      }
    }
  }
}

export default function DonateButton() {
  const container = useRef<HTMLDivElement>(null)
  const [hasError, setHasError] = useState(false)

  function renderButton() {
    // onReady also runs when returning to this route with the SDK already loaded.
    if (!container.current || container.current.hasChildNodes()) return

    try {
      if (!window.PayPal?.Donation) throw new Error("PayPal Donate SDK unavailable")

      window.PayPal.Donation.Button({
        env: "production",
        hosted_button_id: HOSTED_BUTTON_ID,
        image: {
          src: "https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif",
          alt: "Donate with PayPal button",
          title: "PayPal - The safer, easier way to pay online!"
        }
      }).render("#donate-button")

      // The SDK inserts a clickable image; expose the same action to keyboard users.
      const image = container.current.querySelector("img")
      if (image) {
        image.removeAttribute("id")
        image.setAttribute("role", "button")
        image.tabIndex = 0
        image.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault()
            image.click()
          }
        })
      }
    } catch {
      setHasError(true)
    }
  }

  return (
    <div id="donate-button-container" className={styles.buttonContainer}>
      <div id="donate-button" ref={container} />
      <Script
        src="https://www.paypalobjects.com/donate/sdk/donate-sdk.js"
        charSet="UTF-8"
        strategy="afterInteractive"
        onReady={renderButton}
        onError={() => setHasError(true)}
      />
      {hasError && (
        <p role="status" className={styles.paymentNote}>
          The donation button couldn’t load. You can still donate directly through PayPal below.
        </p>
      )}
      <a
        className={styles.link}
        href={`https://www.paypal.com/donate/?hosted_button_id=${HOSTED_BUTTON_ID}`}
      >
        Donate directly on PayPal
      </a>
    </div>
  )
}
