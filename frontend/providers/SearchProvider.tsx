"use client"
import { createContext, useCallback, useContext, useMemo, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { SearchRequest, SearchResponse, PaginatedSearchResponses } from "@/utils/api"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useRouter, useSearchParams } from "next/navigation"

interface SearchContext {
  searchAll: (
    query: Omit<SearchRequest, "access_token" | "accessToken">
  ) => Promise<PaginatedSearchResponses>
  searchResults?: PaginatedSearchResponses
  loading: boolean
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
  const [searchResults, setResults] = useState<PaginatedSearchResponses | undefined>(undefined)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const searchParams = useSearchParams()

  const updateQueryParams = (query: Omit<SearchRequest, "access_token" | "accessToken">) => {
    console.log("Updating query params with:", query)
    const params = new URLSearchParams(searchParams.toString())
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined) {
        console.log({ [key]: value })
        params.set(key, String(value))
      }
    })
    const destination = params.toString()
    router.push(`/search?${destination}`)
    return params
  }

  const searchAll = useCallback(
    async (query: Omit<SearchRequest, "access_token" | "accessToken">) => {
      setLoading(true)
      const params = updateQueryParams(query)
      if (!accessToken) throw new Error("No access token")

      try {
        const apiUrl = `${apiBaseUrl}${API_ROUTES.search.all}`
        const results = await fetch(`${apiUrl}?${params.toString()}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
          }
        })

        // TODO:
        // status check for not found, unauthorized, etc.
        if (!results.ok) {
          throw new Error("Failed to search content")
        }

        const data: PaginatedSearchResponses = await results.json()
        setResults(data)
        return data
      } catch (error) {
        const errorResponse: PaginatedSearchResponses = {
          error: typeof error === "string" || error === null ? error : String(error),
          results: [],
          page: 0,
          per_page: 0,
          pages: 0,
          total: 0
        }
        console.error("Error searching all:", errorResponse)
        return errorResponse
      } finally {
        setLoading(false)
      }
    },
    [accessToken, router]
  )

  return useMemo(() => ({ searchAll, searchResults, loading }), [searchResults, searchAll, loading])
}
