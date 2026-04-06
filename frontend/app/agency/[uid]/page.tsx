"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useParams } from "next/navigation"
import { Agency } from "@/utils/api"
import DetailsLayout from "@/components/Details/DetailsLayout"
import AgencyIdentityCard from "@/components/Details/IdentityCard/AgencyIdentityCard"
import AgencyDetailsTabs from "@/components/Details/tabs/AgencyDetailsTabs"

export default function AgencyDetailsPage() {
  const params = useParams<{ uid: string }>()
  const uid = params.uid

  const [agency, setAgency] = useState<Agency | null>(null)
  const { accessToken } = useAuth()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!accessToken || !uid) return

    setLoading(true)

    apiFetch(
      `${apiBaseUrl}${API_ROUTES.agencies.profile(uid)}?include=complaints&include=officers&include=units&include=reported_units&include=location`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    )
      .then((res) => res.json())
      .then((data) => setAgency(data.results || data))
      .finally(() => setLoading(false))
  }, [accessToken, uid])

  if (loading) return <div>Loading...</div>
  if (!agency) return <div>Agency not found</div>

  return (
    <DetailsLayout>
      <AgencyIdentityCard agency={agency} />
      <AgencyDetailsTabs {...agency} />
    </DetailsLayout>
  )
}
