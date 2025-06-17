"use client"
import { createContext, useCallback, useContext, useMemo, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { IncidentSearchRequest, IncidentSearchResponse } from "@/utils/api"
import API_ROUTES from "@/utils/apiRoutes"

interface SearchContext {
  searchIncidents: (
    query: Omit<IncidentSearchRequest, "access_token" | "accessToken">
  ) => Promise<IncidentSearchResponse>
  incidentResults?: IncidentSearchResponse
}

const SearchContext = createContext<SearchContext | undefined>(undefined)

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const search = useHook()
  return <SearchContext.Provider value={search}>{children}</SearchContext.Provider>
}

export const useSearch = () => {
  const context = useContext(SearchContext)
  if (!context) {
    throw new Error("useSearch must be used within an SearchProvider")
  }
  return context
}

function useHook(): SearchContext {
  const { accessToken } = useAuth()
  const [incidentResults, setResults] = useState<IncidentSearchResponse | undefined>(undefined)

  const searchIncidents = useCallback(
    async (query: Omit<IncidentSearchRequest, "access_token" | "accessToken">) => {
      const { dateStart, dateEnd, ...rest } = query
      if (!accessToken) throw new Error("No access token")

      const formattedDateStart = dateStart
        ? new Date(dateStart).toISOString().slice(0, -1)
        : undefined
      const formattedDateEnd = dateEnd ? new Date(dateEnd).toISOString().slice(0, -1) : undefined

      try {
        const results = await fetch(API_ROUTES.search.incidents, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
          },
          body: JSON.stringify({
            dateStart: formattedDateStart,
            dateEnd: formattedDateEnd,
            ...rest
          })
        })

        // TODO:
        // status check for not found, unauthorized, etc.
        if (!results.ok) {
          throw new Error("Failed to fetch incidents")
        }

        const data: IncidentSearchResponse = await results.json()
        setResults(data)
        return data
      } catch (error) {
        console.error("Error fetching incidents:", error)
        throw error
      }
    },
    [accessToken]
  )

  return useMemo(() => ({ searchIncidents, incidentResults }), [incidentResults, searchIncidents])
}
