"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useParams } from "next/navigation"
import { Officer } from "@/utils/api"
import DetailsLayout from "@/components/Details/DetailsLayout"
import OfficerIdentityCard from "@/components/Details/IdentityCard/OfficerIdentityCard"
import OfficerDetailsTabs from "@/components/Details/tabs/OfficerDetailsTabs"
import OfficerContentDetails from "@/components/Details/ContentDetails/OfficerContentDetails"

export default function OfficerDetailsPage() {
  const params = useParams<{ uid: string }>()
  const uid = params.uid

  const [officer, setOfficer] = useState<Officer | null>(null)
  const { accessToken } = useAuth()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!accessToken || !uid) return

    setLoading(true)

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
  }, [accessToken, uid])

  if (loading) return <div>Loading...</div>
  if (!officer) return <div>Officer not found</div>

  return (
    <DetailsLayout sidebar={<OfficerContentDetails officer={officer} />}>
      <OfficerIdentityCard {...officer} />
      <OfficerDetailsTabs {...officer} />
    </DetailsLayout>
  )
}
