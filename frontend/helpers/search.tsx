import React, { createContext, useCallback, useContext, useMemo, useState } from "react"
import { useAuth } from "./auth"
import * as api from "./api"

interface SearchState {
  searchIncidents: (query: api.IncidentSearchRequest) => Promise<api.IncidentSearchResponse>
  incidentResults?: api.IncidentSearchResponse
}

const SearchContext = createContext<SearchState>(undefined)

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const search = useHook()
  return <SearchContext.Provider value={search}>{children}</SearchContext.Provider>
}

export function useSearch() {
  return useContext(SearchContext)
}

function useHook(): SearchState {
  const { accessToken } = useAuth()
  const [incidentResults, setResults] = useState<api.IncidentSearchResponse>(undefined)

  const searchIncidents = useCallback(
    async (query: Omit<api.IncidentSearchRequest, "access_token">) => {
      const results = await api.searchIncidents({ accessToken, ...query })
      setResults(results)
      return results
    },
    [accessToken]
  )

  return useMemo(() => ({ searchIncidents, incidentResults }), [incidentResults, searchIncidents])
}
