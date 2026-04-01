"use client"

import { useEffect, useRef, useState } from "react"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { Officer } from "@/utils/api"
import { useAuth } from "@/providers/AuthProvider"

export function useUnitOfficers(unitUid: string | undefined, enabled: boolean) {
  const { accessToken } = useAuth()
  const [officers, setOfficers] = useState<Officer[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<Error | null>(null)
  const fetchedRef = useRef(false)

  useEffect(() => {
    if (!enabled || fetchedRef.current || !unitUid || !accessToken) return

    const url = `${apiBaseUrl}${API_ROUTES.agencies.profile(unitUid)}/officers?page=1&per_page=25&include=employment`

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
        setOfficers(data.results ?? [])
      })
      .catch((err) => setError(err instanceof Error ? err : new Error(String(err))))
      .finally(() => setLoading(false))
  }, [accessToken, enabled, unitUid])

  return { officers, loading, error }
}
