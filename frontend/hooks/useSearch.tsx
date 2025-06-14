import React, { createContext, useCallback, useContext, useMemo, useState } from "react"
import { useAuth } from "@/context/AuthProvider"
import * as api from "@/utils/api"
import { IncidentSearchRequest, IncidentSearchResponse, searchIncidents } from "@/utils/api"

interface SearchState {
  searchIncidents: (query: api.IncidentSearchRequest) => Promise<api.IncidentSearchResponse>
  incidentResults?: api.IncidentSearchResponse
}

const SearchContext = createContext<SearchState | undefined>(undefined)

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const search = useHook()
  return <SearchContext.Provider value={search}>{children}</SearchContext.Provider>
}

export function useSearch() {
  return useContext(SearchContext)
}

function useHook(): SearchState {
  const { token } = useAuth()
  const [incidentResults, setResults] = useState<api.IncidentSearchResponse | undefined>(undefined)

  const searchIncidents = useCallback(
    async (query: Omit<api.IncidentSearchRequest, "access_token">) => {
      const results = await searchIncidents({ token, ...query })
      setResults(results)
      return results
    },
    [token]
  )

  return useMemo(() => ({ searchIncidents, incidentResults }), [incidentResults, searchIncidents])
}