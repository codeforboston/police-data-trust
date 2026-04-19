"use client"

import { useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

export default function OrganizationPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const slug = searchParams.get("slug")

  useEffect(() => {
    if (slug) {
      router.replace(`/sources/${slug}`)
      return
    }

    router.replace("/404")
  }, [router, slug])

  return <div className="p-4">Redirecting...</div>
}
