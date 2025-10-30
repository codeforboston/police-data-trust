"use client"
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"
import { useAuth } from "@/providers/AuthProvider"
import { SearchRequest, SearchResponse, PaginatedSearchResponses, SearchParams } from "@/utils/api"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useRouter, useSearchParams } from "next/navigation"

interface SearchContext {
  searchAll: (
    request: SearchParams
  ) => Promise<PaginatedSearchResponses>
  searchResults?: PaginatedSearchResponses
  loading: boolean,
  searchState: SearchParams | undefined
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
  const [searchState, setSearchState] = useState<SearchParams | undefined>()
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const searchParams = useSearchParams()

  // Get parameters from url and sync searchState from it - sync it on mount and in-between back/forth navigation
  useEffect(() => {
    // handle array params like ?location=NYC&location=Texas
    const params: Record<string, any> = {}
    searchParams.entries().forEach(([key, value]) => {
      if (params[key]) {
        // Add to array or create it as needed
        if (Array.isArray(params[key])) {
          params[key].push(value)
        } else {
          params[key] = [params[key], value]
        }
      } else {
        params[key] = value
      }
    })
    
    setSearchState(params as SearchParams)
  }, [searchParams])

  // Auto-fetch whenever there's a manual URL change
  useEffect(() => {
    if (searchState && Object.keys(searchState).length) {
      searchAll(searchState)
    }
  }, [searchState])

  // Update both search state and URL upon call in search function
  const updateQueryParams = (request: SearchParams) => { // TODO: where's the "access_token" one coming from?
    console.log("Updating query params with:", request)
    const params = new URLSearchParams()
    Object.entries(request).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach((v) => params.append(key, v)) // Convert list into url params like ?location=NYC&location=Texas
        } else {
          params.set(key, String(value))
        }
      }
    })
    const destination = params.toString()
    router.push(`/search?${destination}`)
    setSearchState(request) // Update state along the URL
    return params
  }

  // TODO: Don't allow multiple tries until previous load finishes
  // Main search function  
  const searchAll = useCallback(
    async (request: SearchParams) => {

      setLoading(true)
      const params = updateQueryParams(request) // Update url AND search state upon new search

      try {
        const apiUrl = `${apiBaseUrl}${API_ROUTES.search.all}`
        const results = await fetch(`${apiUrl}?${params.toString()}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
          }
        })

        // TODO: status check for not found, unauthorized, etc.
        if (!results.ok) throw new Error("Failed to search content")
        
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

  return useMemo(() => ({ searchAll, searchResults, loading, searchState }), [searchResults, searchAll, loading, searchState])
}
