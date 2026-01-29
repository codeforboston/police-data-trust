"use client"
import { createContext, useCallback, useContext, useMemo, useState, useEffect, useRef } from "react"
import { apiFetch } from "@/utils/apiFetch"
import { useAuth } from "@/providers/AuthProvider"
import { SearchRequest, SearchResponse, PaginatedSearchResponses } from "@/utils/api"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { ApiError } from "@/utils/apiError"
import { useRouter, useSearchParams } from "next/navigation"
import { getParamKeys } from "./config"

interface SearchContext {
  searchAll: (
    query: Omit<SearchRequest, "access_token" | "accessToken">
  ) => Promise<PaginatedSearchResponses>
  searchResults?: PaginatedSearchResponses
  loading: boolean
  error: string | null
  setPage: (page: number) => void
  tab: number
  updateTab: (tab: number) => void
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
  const { accessToken, refreshAccessToken } = useAuth()
  const [searchResults, setResults] = useState<PaginatedSearchResponses | undefined>(undefined)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<number>(0)
  const router = useRouter()
  const searchParams = useSearchParams()

  // AbortController ref to cancel in-flight requests
  const abortControllerRef = useRef<AbortController | null>(null)

  // Track if we should skip the effect (when searchAll handles the fetch)
  const skipEffectRef = useRef(false)

  // Helper to update URL search params. Returns the new URLSearchParams object.
  const updateQueryParams = useCallback(
    (tab: number, updates: Record<string, any>) => {
      const params = new URLSearchParams(searchParams.toString())
      Object.entries(updates).forEach(([key, value]) => {
        if (value === undefined || value === null) {
          params.delete(key)
        } else {
          params.set(key, String(value))
        }
      })
      const destination = params.toString()
      router.push(`/search?${destination}`)
      return params
    },
    [searchParams, router]
  )

  // Build a SearchRequest-like payload from URLSearchParams
  const buildRequestFromParams = useCallback((params: URLSearchParams) => {
    const q = params.get("query") || ""
    const location = params.get("location") || undefined
    const source = params.get("source") || undefined
    const pageStr = params.get("page")
    const page = pageStr ? Number(pageStr) : undefined
    const payload: Omit<SearchRequest, "access_token" | "accessToken"> = { query: q }
    if (location) payload.location = location
    if (source) payload.source = source
    if (page !== undefined) payload.page = page
    return payload
  }, [])

  const getSearchType = (tab: number) => {
    switch (tab) {
      case 1:
        return API_ROUTES.search.officers
      default:
        return API_ROUTES.search.all
    }
  }

  const updateTab = (sel: number) => {
    setTab(sel)
  }

  // Fetch based on provided URLSearchParams (or current searchParams if omitted)
  const fetchFromParams = useCallback(
    async (params: URLSearchParams, updatedTab?: number, signal?: AbortSignal) => {
      if (!accessToken) {
        const errorResponse: PaginatedSearchResponses = {
          error: "No access token available",
          results: []
        }
        setError("No access token available")
        setResults(errorResponse)
        return errorResponse
      }

      setLoading(true)
      setError(null)

      try {
        let apiUrl = apiBaseUrl;
        // need to update params for api call if tab has changed
        if (updatedTab) {
          const oldParams = params.toString().split('=')[1];
          const paramKeys = getParamKeys(updatedTab);
          const newParams = new URLSearchParams();
          paramKeys.forEach((key: string) => newParams.set(key, oldParams));
          if (updatedTab !== 0) {
            // needed to get back search result type data from API
            newParams.set('searchResult', 'true');
          }
          apiUrl += `${getSearchType(updatedTab)}?${newParams.toString()}`
        } else {
          apiUrl += `${getSearchType(tab)}?${params.toString()}`
        }
        const response = await apiFetch(apiUrl, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          signal
        })

        if (!response.ok) {
          throw new Error(`Failed to search content: ${response.statusText}`)
        }

        const data: PaginatedSearchResponses = await response.json()
        setResults(data)
        setError(null)
        return data
      } catch (err) {
        // Don't set error if request was aborted
        if (err instanceof Error && err.name === "AbortError") {
          return { results: [] }
        }

        const errorMessage = err instanceof Error ? err.message : String(err)
        const errorResponse: PaginatedSearchResponses = {
          error: errorMessage,
          results: []
        }
        setError(errorMessage)
        setResults(errorResponse)
        return errorResponse
      } finally {
        setLoading(false)
      }
    },
    [accessToken]
  )

  const searchAll = useCallback(
    async (query: Omit<SearchRequest, "access_token" | "accessToken">) => {
      // Cancel any in-flight request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }

      // Create new AbortController for this request
      const abortController = new AbortController()
      abortControllerRef.current = abortController

      // Set flag to skip the effect's fetch (we're handling it here)
      skipEffectRef.current = true

      // Update URL params
      const params = updateQueryParams(tab, query as Record<string, any>)

      // Fetch directly
      const data = await fetchFromParams(params, undefined, abortController.signal)
      return data
    },
    [updateQueryParams, fetchFromParams]
  )

  const setPage = useCallback(
    (page: number) => {
      // Validate page number
      if (page < 1) {
        setError("Page number must be at least 1")
        return
      }

      if (searchResults?.pages && page > searchResults.pages) {
        setError(`Page ${page} exceeds maximum pages (${searchResults.pages})`)
        return
      }

      // Update the page param in the URL. The effect watching params will trigger a fetch.
      updateQueryParams(tab, { page })
    },
    [updateQueryParams, searchResults?.pages]
  )

  //Effect: when new tab is clicked, fetch results
  useEffect(() => {
    // check if we should skip
    if (skipEffectRef.current) {
      skipEffectRef.current = false;
      return;
    }

    // cancel any in flight requests
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    fetchFromParams(searchParams, tab, abortController.signal).catch((err) => {
      // only log non abort errors
      if (!(err instanceof Error && err.name === 'AbortError')) {
        console.error("fetchFromParams on tab change effect error", err)
      }
    })

    // Cleanup: abort on unmount or param change
    return () => {
      abortController.abort()
    }
  }, [tab])

  // Effect: when searchParams change, fetch results
  useEffect(() => {
    // Check if we should skip (searchAll already handled the fetch)
    if (skipEffectRef.current) {
      skipEffectRef.current = false
      return
    }

    const paramsString = searchParams.toString()

    // Don't fetch if there are no search params
    if (!paramsString) {
      return
    }

    // Cancel any in-flight request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new AbortController for this request
    const abortController = new AbortController()
    abortControllerRef.current = abortController

    const params = new URLSearchParams(paramsString)
    fetchFromParams(params, undefined, abortController.signal).catch((err) => {
      // Only log non-abort errors
      if (!(err instanceof Error && err.name === "AbortError")) {
        console.error("fetchFromParams effect error", err)
      }
    })

    // Cleanup: abort on unmount or param change
    return () => {
      abortController.abort()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams])

  return useMemo(
    () => ({ searchAll, searchResults, loading, error, setPage, updateTab, tab }),
    [searchResults, searchAll, loading, error, setPage, updateTab, tab]
  )
}
