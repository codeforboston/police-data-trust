"use client"

import { useEffect, useRef, useState } from "react"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { SearchResponse } from "@/utils/api"
import { useAuth } from "@/providers/AuthProvider"

export function useUnitOfficers(unitUid: string | undefined, enabled: boolean) {
  const { accessToken } = useAuth()
  const [officers, setOfficers] = useState<SearchResponse[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<Error | null>(null)
  const fetchedRef = useRef(false)

  useEffect(() => {
    if (!enabled || fetchedRef.current || !unitUid || !accessToken) return

    fetchedRef.current = true
    setLoading(true)
    setError(null)

    // /api/v1/agencies/52192a89b0144fe6bf624239ed16d5db/officers?page=268&include=employment&per_page=1
    apiFetch(
      `${apiBaseUrl}${API_ROUTES.agencies.profile(unitUid)}/officers?page=1&per_page=25&include=employment`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    )
      .then((res) => res.json())
      .then((data) => {
        setOfficers(data.results ?? [])
      })
      .catch((err) => setError(err instanceof Error ? err : new Error(String(err))))
      .finally(() => setLoading(false))
  }, [accessToken, enabled, unitUid])

  return { officers, loading, error }
}
