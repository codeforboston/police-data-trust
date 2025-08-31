"use client"
import React from "react"
import { useRouter, useSearchParams } from "next/navigation"
import Box from "@mui/material/Box"
import Stack from "@mui/material/Stack"
import Link from "@mui/material/Link"
import Button from "@mui/material/Button"
import Image from "next/image"
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import styles from "./registrationError.module.css"

type ErrorCode =
  | "EMAIL_TAKEN"
  | "TOKEN_INVALID"
  | "TOKEN_EXPIRED"
  | "RATE_LIMIT"
  | "SERVER"
  | "NETWORK"
  | "UNKNOWN"

const ERROR_CATALOG: Record<
  ErrorCode,
  { title: string; message: string; primaryCta?: { label: string; href: string } }
> = {
  EMAIL_TAKEN: {
    title: "This email is already registered",
    message: "Try signing in instead. If you don’t remember your password, you can reset it.",
    primaryCta: { label: "Go to Sign In", href: "/login" }
  },
  TOKEN_INVALID: {
    title: "Invalid or malformed verification link",
    message:
      "The link you used doesn’t look right. Request a new verification email and try again.",
    primaryCta: { label: "Resend verification", href: "/register/resend" }
  },
  TOKEN_EXPIRED: {
    title: "Your verification link has expired",
    message:
      "For security, verification links expire after a while. Request a new one and try again.",
    primaryCta: { label: "Resend verification", href: "/register/resend" }
  },
  RATE_LIMIT: {
    title: "Too many attempts",
    message: "You’ve made too many requests in a short time. Please wait a bit and try again.",
    primaryCta: { label: "Return Home", href: "/" }
  },
  NETWORK: {
    title: "Network error",
    message: "We couldn’t reach the server. Check your connection and try again.",
    primaryCta: { label: "Try again", href: "/register" }
  },
  SERVER: {
    title: "We had a problem on our side",
    message: "Our servers hit a snag while processing your request. Please try again in a moment.",
    primaryCta: { label: "Try again", href: "/register" }
  },
  UNKNOWN: {
    title: "Something went wrong…",
    message:
      "We weren’t able to complete your registration. Please try again. If the problem persists, contact our team.",
    primaryCta: { label: "Return Home", href: "/" }
  }
}

export default function RegistrationError() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const code = (searchParams.get("code") as ErrorCode) || "UNKNOWN"
  const rid = searchParams.get("rid") || undefined // request/incident id from backend if available
  const debug = searchParams.get("debug") === "1" || process.env.NODE_ENV !== "production"

  const { title, message, primaryCta } = ERROR_CATALOG[code] ?? ERROR_CATALOG.UNKNOWN

  const supportHref = (() => {
    const dest = "/contact" // or mailto:support@npdc.org
    // If using mailto:, include code/rid in subject/body
    return dest
  })()

  // Optional: keep users on the page while retrying (if you have a one-click retry)
  const [retrying, setRetrying] = React.useState(false)
  const onRetry = () => {
    setRetrying(true)
    router.replace("/register")
  }

  return (
    <div>
      <Box
        role="alert"
        aria-live="assertive"
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "84vh",
          flexDirection: "column",
          textAlign: "center",
          px: 2
        }}
      >
        <Image src={logo} alt="NPDC Logo" width={100} height={100} priority />
        <h1 className={styles.h1}>{title}</h1>
        <p className={styles.p}>{message}</p>

        {/* Helpful context for support/correlation */}
        <p className={styles.p} style={{ opacity: 0.8 }}>
          {rid ? (
            <>
              {" "}
              • Reference ID: <code>{rid}</code>
            </>
          ) : null}
        </p>

        <Stack spacing={2} mt={2} alignItems="center">
          {/* Row 1: primary CTA or retry */}
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap">
            {primaryCta ? (
              <Link href={primaryCta.href} underline="none">
                <Button variant="contained" disabled={retrying}>
                  {primaryCta.label}
                </Button>
              </Link>
            ) : (
              <Button variant="contained" onClick={onRetry} disabled={retrying}>
                Try again
              </Button>
            )}
          </Stack>

          {/* Row 2: secondary actions */}
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap">
            <Link href="/" className={styles.link} underline="none">
              <Button variant="text">Return Home</Button>
            </Link>
            <Link href={supportHref} className={styles.link} underline="none">
              <Button variant="text">Contact Support</Button>
            </Link>
          </Stack>
        </Stack>

        {/* Optional: technical details for dev/staging or debug=1 */}
        {debug && (
          <details style={{ marginTop: 16 }}>
            <summary>Technical details</summary>
            <pre
              style={{
                textAlign: "left",
                marginTop: 8,
                maxWidth: 640,
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                opacity: 0.9
              }}
            >
              {`path: /register/error
code: ${code}
rid: ${rid ?? "(none)"} 
ts: ${new Date().toISOString()}`}
            </pre>
          </details>
        )}
      </Box>
    </div>
  )
}
