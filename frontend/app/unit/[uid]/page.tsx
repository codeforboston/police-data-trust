"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useParams } from "next/navigation"
import { Unit } from "@/utils/api"
import DetailsLayout from "@/components/Details/DetailsLayout"
import UnitIdentityCard from "@/components/Details/IdentityCard/UnitIdentityCard"
import UnitDetailsTabs from "@/components/Details/tabs/UnitDetailsTabs"
import UnitContentDetails from "@/components/Details/ContentDetails/UnitContentDetails"

export default function UnitDetailsPage() {
  const params = useParams<{ uid: string }>()
  const uid = params.uid

  const [unit, setUnit] = useState<Unit | null>(null)
  const { accessToken } = useAuth()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!accessToken || !uid) return

    setLoading(true)

    apiFetch(
      `${apiBaseUrl}${API_ROUTES.units.profile(uid)}?include=officers&include=reported_officers&include=complaints&include=location`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    )
      .then((res) => res.json())
      .then((data) => setUnit(data.results || data))
      .finally(() => setLoading(false))
  }, [accessToken, uid])

  if (loading) return <div>Loading...</div>
  if (!unit) return <div>Unit not found</div>

  return (
    <DetailsLayout sidebar={<UnitContentDetails unit={unit} />}>
      <UnitIdentityCard unit={unit} />
      <UnitDetailsTabs {...unit} />
    </DetailsLayout>
  )
}
