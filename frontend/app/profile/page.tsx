"use client"

import React, { useEffect } from "react"
import { useUserProfile } from "@/utils/useProfile"
import { useRouter } from "next/navigation"

export default function ProfilePage() {
  const { profile, loading } = useUserProfile()
  const router = useRouter()

  useEffect(() => {
    if (profile?.uid) {
      router.replace(`/profile/${profile.uid}`)
    }
  }, [profile?.uid, router])

  if (loading) return <p>Loading profile...</p>
  return <p>Redirecting...</p>
}
