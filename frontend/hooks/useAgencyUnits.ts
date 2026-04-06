"use client"

import { useEffect, useRef, useState } from "react"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { Unit } from "@/utils/api"
import { useAuth } from "@/providers/AuthProvider"

export function useAgencyUnits(agencyUid: string | undefined, enabled: boolean) {
  const { accessToken } = useAuth()
  const [units, setUnits] = useState<Unit[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<Error | null>(null)
  const fetchedRef = useRef(false)

  useEffect(() => {
    if (!enabled || fetchedRef.current || !agencyUid || !accessToken) return

    const url = `${apiBaseUrl}${API_ROUTES.agencies.profile(agencyUid)}/units?page=1&per_page=25`

    fetchedRef.current = true
    setLoading(true)
    setError(null)
    apiFetch(url, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
      .then((res) => res.json())
      .then((data) => {
        setUnits(data.results ?? [])
      })
      .catch((err) => setError(err instanceof Error ? err : new Error(String(err))))
      .finally(() => setLoading(false))
  }, [accessToken, enabled, agencyUid])

  return { units, loading, error }
}
