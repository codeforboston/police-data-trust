"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useSearchParams } from "next/navigation"
import { Officer } from "@/utils/api"
import DetailsLayout from "@/components/Details/DetailsLayout"
import IdentityCard from "@/components/Details/IdentityCard"
import DetailsTabs from "@/components/Details/DetailsTabs"
import ContentDetails from "@/components/Details/ContentDetails"

export default function OfficerDetailsPage() {
  const searchParams = useSearchParams()
  const uid = searchParams.get("uid")
  const [officer, setOfficer] = useState<Officer | null>(null)
  const { accessToken } = useAuth()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (accessToken && uid) {
      apiFetch(
        `${apiBaseUrl}${API_ROUTES.officers.profile(uid)}?include=employment&include=allegations`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        }
      )
        .then((res) => res.json())
        .then((data) => setOfficer(data.results || data))
        .finally(() => setLoading(false))
    }
  }, [accessToken, uid])

  if (loading) return <div>Loading...</div>
  if (!officer) return <div>Officer not found</div>

  return (
    <DetailsLayout sidebar={<ContentDetails officer={officer} />}>
      <IdentityCard {...officer} />
      <DetailsTabs {...officer} />
    </DetailsLayout>
  )
}
