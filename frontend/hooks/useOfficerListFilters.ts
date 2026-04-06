"use client"

import { useCallback, useState } from "react"

export type OfficerListFilters = {
  searchTerm: string
  status: string[]
  rank: string[]
  type: string[]
  unit: string[]
}

export const DEFAULT_OFFICER_LIST_FILTERS: OfficerListFilters = {
  searchTerm: "",
  status: [],
  rank: [],
  type: [],
  unit: []
}

export function mergeOfficerListFilters(
  currentFilters: OfficerListFilters,
  updates: Partial<OfficerListFilters>
) {
  return { ...currentFilters, ...updates }
}

export function useOfficerListFilters(
  initialFilters: OfficerListFilters = DEFAULT_OFFICER_LIST_FILTERS
) {
  const [filters, setFilters] = useState<OfficerListFilters>(initialFilters)

  const updateFilters = useCallback((updates: Partial<OfficerListFilters>) => {
    setFilters((currentFilters) => mergeOfficerListFilters(currentFilters, updates))
  }, [])

  return { filters, setFilters, updateFilters }
}
