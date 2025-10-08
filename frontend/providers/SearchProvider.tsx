"use client"
import { createContext, useCallback, useContext, useMemo, useState } from "react"
import { apiFetch } from "@/utils/apiFetch"
import { useAuth } from "@/providers/AuthProvider"
import { SearchRequest, PaginatedSearchResponses } from "@/utils/api"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { ApiError } from "@/utils/apiError"
import { useRouter, useSearchParams } from "next/navigation"

interface SearchContext {
  searchAll: (
    query: Omit<SearchRequest, "access_token" | "accessToken">
  ) => Promise<PaginatedSearchResponses>
  searchResults?: PaginatedSearchResponses
  loading: boolean
  updateView: (val: string) => void
  view: string
}

const SearchContext = createContext<SearchContext | undefined>(undefined)

const getViewParams = (view: string, query: string) => {
  switch (view) {
    case "officers":
      return `name=${query}&agency=${query}`
  }
}

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
  const [view, setView] = useState("all")
  const [queryValue, setQueryValue] = useState("")
  const router = useRouter()
  const searchParams = useSearchParams()

  const updateView = (val: string) => {
    setView(val)
    searchAll({ query: queryValue }, val)
  }

  const updateQueryParams = (query: Omit<SearchRequest, "access_token" | "accessToken">) => {
    console.log("Updating query params with:", query)
    setQueryValue(query.query)
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
    async (query: Omit<SearchRequest, "access_token" | "accessToken">, viewUpdate?: string) => {
      if (!accessToken) throw new ApiError("No access token", "NO_ACCESS_TOKEN", 401)
      setLoading(true)

      try {
        const params = updateQueryParams(query)
        let apiUrl = ""
        if (viewUpdate && viewUpdate !== "all") {
          apiUrl = `${apiBaseUrl}/${viewUpdate}?${getViewParams(viewUpdate, query.query)}`
        } else {
          apiUrl = `${apiBaseUrl}${API_ROUTES.search.all}?${params?.toString()}`
        }

        const response = await apiFetch(apiUrl, {
          method: "GET",
          headers: {
            "Content-Type": "application/json"
          }
        })

        // TODO:
        // status check for not found, unauthorized, etc.
        if (!response.ok) {
          throw new Error("Failed to search content")
        }

        const data: PaginatedSearchResponses = await response.json()
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
    [accessToken, refreshAccessToken, router]
  )

  return useMemo(
    () => ({ searchAll, searchResults, loading, updateView, view }),
    [searchResults, searchAll, loading, updateView, view]
  )
}
