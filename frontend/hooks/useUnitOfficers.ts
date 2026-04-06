"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { Officer } from "@/utils/api"
import { useAuth } from "@/providers/AuthProvider"

export type UnitOfficerQueryParams = {
  page?: number
  per_page?: number
  term?: string
  type?: string[]
  status?: string[]
  rank?: string[]
  include?: string[]
}

function buildUnitOfficerUrl(unitUid: string, params: UnitOfficerQueryParams = {}) {
  const search = new URLSearchParams()

  search.set("page", String(params.page ?? 1))
  search.set("per_page", String(params.per_page ?? 25))

  if (params.term?.trim()) {
    search.set("term", params.term.trim())
  }

  for (const value of params.type ?? []) {
    search.append("type", value)
  }

  for (const value of params.status ?? []) {
    search.append("status", value)
  }

  for (const value of params.rank ?? []) {
    search.append("rank", value)
  }

  for (const value of params.include ?? []) {
    search.append("include", value)
  }

  return `${apiBaseUrl}${API_ROUTES.units.profile(unitUid)}/officers?${search.toString()}`
}

export function useUnitOfficers(
  unitUid: string | undefined,
  enabled: boolean,
  params: UnitOfficerQueryParams = {}
) {
  const { accessToken } = useAuth()
  const [officers, setOfficers] = useState<Officer[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<Error | null>(null)
  const fetchedRef = useRef(false)

  const url = useMemo(() => {
    if (!unitUid) return null
    return buildUnitOfficerUrl(unitUid, {
      include: ["employment"],
      ...params
    })
  }, [unitUid, params])

  useEffect(() => {
    if (!enabled || !unitUid || !accessToken || !url) return

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
  }, [accessToken, enabled, unitUid, url])

  return { officers, loading, error }
}
