"use client"
import React from "react"
import Success from "@/components/Success/Success"

export default function ForgotPasswordSuccessfull() {
  const copy =
    "If this email matches an existing account, you will receive an email with instructions to reset your password."
  return (
    <div>
      <Success copy={copy} />
    </div>
  )
}
