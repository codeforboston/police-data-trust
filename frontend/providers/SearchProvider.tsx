"use client"

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { apiFetch } from "@/utils/apiFetch"
import { useAuth } from "@/providers/AuthProvider"
import { PaginatedSearchResponses } from "@/utils/api"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"

export type SearchTab = "all" | "officers" | "agencies" | "units"

export type SearchFilters = {
  city: string[]
  cityUid: string[]
  source: string[]
  sourceUid: string[]
}

export type SearchState = {
  term: string
  tab: SearchTab
  page: number
} & SearchFilters

type SearchStatePatch = Partial<SearchState>

interface SearchContext {
  state: SearchState
  searchResults?: PaginatedSearchResponses
  loading: boolean
  error: string | null
  setTerm: (term: string) => void
  setPage: (page: number) => void
  setTab: (tab: SearchTab) => void
  setFilters: (filters: Partial<SearchFilters>) => void
}

const DEFAULT_FILTERS: SearchFilters = {
  city: [],
  cityUid: [],
  source: [],
  sourceUid: []
}

const DEFAULT_STATE: SearchState = {
  term: "",
  tab: "all",
  page: 1,
  ...DEFAULT_FILTERS
}

const SEARCH_TABS: SearchTab[] = ["all", "officers", "agencies", "units"]

const SearchContext = createContext<SearchContext | undefined>(undefined)

const getNormalizedString = (value?: string | null) => {
  if (value === null || value === undefined) {
    return undefined
  }

  const trimmed = value.trim()
  return trimmed === "" ? undefined : trimmed
}

const normalizeStringList = (values?: string[] | null) =>
  (values ?? []).map((value) => value.trim()).filter(Boolean)

const getSearchRoute = (tab: SearchTab) => {
  switch (tab) {
    case "officers":
      return API_ROUTES.search.officers
    case "agencies":
      return API_ROUTES.search.agencies
    case "units":
      return API_ROUTES.search.units
    default:
      return API_ROUTES.search.all
  }
}

const parseTab = (value?: string | null): SearchTab => {
  if (value && SEARCH_TABS.includes(value as SearchTab)) {
    return value as SearchTab
  }

  return DEFAULT_STATE.tab
}

const parsePage = (value?: string | null) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) && parsed >= 1 ? parsed : DEFAULT_STATE.page
}

type SearchParamReader = {
  get: (name: string) => string | null
  getAll?: (name: string) => string[]
}

const getAllParams = (searchParams: SearchParamReader, name: string) =>
  normalizeStringList(searchParams.getAll?.(name))

const normalizeFilters = (filters: Partial<SearchFilters>): SearchFilters => ({
  city: normalizeStringList(filters.city),
  cityUid: normalizeStringList(filters.cityUid),
  source: normalizeStringList(filters.source),
  sourceUid: normalizeStringList(filters.sourceUid)
})

export const parseSearchState = (searchParams: SearchParamReader): SearchState => {
  const legacyTerm =
    searchParams.get("term") ?? searchParams.get("query") ?? searchParams.get("name")

  const city = getAllParams(searchParams, "city")
  const source = getAllParams(searchParams, "source")

  return {
    term: getNormalizedString(legacyTerm) ?? DEFAULT_STATE.term,
    tab: parseTab(searchParams.get("tab")),
    page: parsePage(searchParams.get("page")),
    city: city.length > 0 ? city : normalizeStringList([searchParams.get("location") ?? ""]),
    cityUid: getAllParams(searchParams, "city_uid"),
    source: source.length > 0 ? source : normalizeStringList([searchParams.get("source") ?? ""]),
    sourceUid: getAllParams(searchParams, "source_uid")
  }
}

const appendListParams = (params: URLSearchParams, key: string, values: string[]) => {
  values.forEach((value) => {
    params.append(key, value)
  })
}

const buildSearchParams = (state: SearchState) => {
  const params = new URLSearchParams()

  if (state.term) {
    params.set("term", state.term)
  }

  if (state.tab !== DEFAULT_STATE.tab) {
    params.set("tab", state.tab)
  }

  if (state.page !== DEFAULT_STATE.page) {
    params.set("page", String(state.page))
  }

  appendListParams(params, "city", state.city)
  appendListParams(params, "city_uid", state.cityUid)
  appendListParams(params, "source", state.source)
  appendListParams(params, "source_uid", state.sourceUid)

  return params
}

export const buildApiParams = (state: SearchState) => {
  const params = new URLSearchParams()

  if (state.term) {
    params.set("term", state.term)
  }

  if (state.page > 1) {
    params.set("page", String(state.page))
  }

  appendListParams(params, "city", state.city)
  appendListParams(params, "city_uid", state.cityUid)
  appendListParams(params, "source", state.source)
  appendListParams(params, "source_uid", state.sourceUid)

  if (state.tab !== "all") {
    params.set("searchResult", "true")
  }

  return params
}

const hasSearchCriteria = (state: SearchState) => {
  return Boolean(
    state.term ||
      state.city.length > 0 ||
      state.cityUid.length > 0 ||
      state.source.length > 0 ||
      state.sourceUid.length > 0
  )
}

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const search = useSearchController()
  return <SearchContext.Provider value={search}>{children}</SearchContext.Provider>
}

export const useSearch = () => {
  const context = useContext(SearchContext)
  if (!context) {
    throw new Error("useSearch must be used within an SearchProvider")
  }
  return context
}

function useSearchController(): SearchContext {
  const { accessToken, hasHydrated } = useAuth()
  const [searchResults, setResults] = useState<PaginatedSearchResponses | undefined>(undefined)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const searchParams = useSearchParams()
  const abortControllerRef = useRef<AbortController | null>(null)

  const state = useMemo(() => parseSearchState(searchParams), [searchParams])

  const updateSearchState = useCallback(
    (patch: SearchStatePatch, options?: { resetPage?: boolean }) => {
      const nextState: SearchState = {
        ...state,
        ...patch,
        ...normalizeFilters({
          city: patch.city ?? state.city,
          cityUid: patch.cityUid ?? state.cityUid,
          source: patch.source ?? state.source,
          sourceUid: patch.sourceUid ?? state.sourceUid
        })
      }

      if (options?.resetPage) {
        nextState.page = DEFAULT_STATE.page
      }

      const normalizedState: SearchState = {
        term: getNormalizedString(nextState.term) ?? DEFAULT_STATE.term,
        tab: parseTab(nextState.tab),
        page: nextState.page >= 1 ? nextState.page : DEFAULT_STATE.page,
        ...normalizeFilters(nextState)
      }

      const destination = buildSearchParams(normalizedState).toString()
      router.push(destination ? `/search?${destination}` : "/search")
    },
    [router, state]
  )

  const setTerm = useCallback(
    (term: string) => {
      updateSearchState({ term }, { resetPage: true })
    },
    [updateSearchState]
  )

  const setTab = useCallback(
    (tab: SearchTab) => {
      updateSearchState({ tab }, { resetPage: true })
    },
    [updateSearchState]
  )

  const setFilters = useCallback(
    (filters: Partial<SearchFilters>) => {
      updateSearchState(filters, { resetPage: true })
    },
    [updateSearchState]
  )

  const setPage = useCallback(
    (page: number) => {
      if (page < 1) {
        setError("Page number must be at least 1")
        return
      }

      if (searchResults?.pages && page > searchResults.pages) {
        setError(`Page ${page} exceeds maximum pages (${searchResults.pages})`)
        return
      }

      updateSearchState({ page })
    },
    [searchResults?.pages, updateSearchState]
  )

  useEffect(() => {
    if (!hasHydrated) {
      return
    }

    if (!accessToken) {
      setLoading(false)
      setResults(undefined)
      return
    }

    if (!hasSearchCriteria(state)) {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }

      setLoading(false)
      setError(null)
      setResults(undefined)
      return
    }

    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    const abortController = new AbortController()
    abortControllerRef.current = abortController

    const fetchSearchResults = async () => {
      setLoading(true)
      setError(null)

      try {
        const apiUrl = `${apiBaseUrl}${getSearchRoute(state.tab)}?${buildApiParams(state).toString()}`
        const response = await apiFetch(apiUrl, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          signal: abortController.signal
        })

        if (!response.ok) {
          throw new Error(`Failed to search content: ${response.statusText}`)
        }

        const data: PaginatedSearchResponses = await response.json()
        setResults(data)
        setError(null)
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          return
        }

        const errorMessage = err instanceof Error ? err.message : String(err)
        setError(errorMessage)
        setResults({
          error: errorMessage,
          results: []
        })
      } finally {
        setLoading(false)
      }
    }

    fetchSearchResults().catch((err) => {
      if (!(err instanceof Error && err.name === "AbortError")) {
        console.error("fetchSearchResults effect error", err)
      }
    })

    return () => {
      abortController.abort()
    }
  }, [accessToken, hasHydrated, state])

  return useMemo(
    () => ({ state, searchResults, loading, error, setTerm, setPage, setTab, setFilters }),
    [error, loading, searchResults, setFilters, setPage, setTab, setTerm, state]
  )
}
