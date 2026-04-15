"use client"

import { type ReactNode, useEffect, useMemo, useState } from "react"
import TextField from "@mui/material/TextField"
import styles from "./filter.module.css"
import {
  Checkbox,
  CircularProgress,
  InputAdornment,
  FormGroup,
  Box,
  Button,
  FormControlLabel,
  Typography
} from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useAuth } from "@/providers/AuthProvider"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"

type CityOption = {
  uid: string
  name: string
  state?: {
    abbreviation?: string
    name?: string
  }
}

type SourceOption = {
  uid: string
  name: string
}

type FilterItem = {
  id: string
  title: string
  checked: boolean
  onToggle: () => void
}

const formatCityLabel = (city: CityOption) =>
  city.state?.abbreviation ? `${city.name}, ${city.state.abbreviation}` : city.name

const fetchFilterOptions = async (url: string, accessToken: string, signal: AbortSignal) => {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    signal
  })

  if (!response.ok) {
    throw new Error(`Failed to load filter options: ${response.status} ${response.statusText}`)
  }

  return response.json()
}

const isBenignFilterFetchError = (error: unknown, signal: AbortSignal) => {
  if (signal.aborted) {
    return true
  }

  return error instanceof Error && error.name === "AbortError"
}

const Filter = () => {
  const {
    state: { tab, city, cityUid, source, sourceUid },
    setFilters
  } = useSearch()
  const { accessToken, hasHydrated } = useAuth()
  const [citySearch, setCitySearch] = useState("")
  const [sourceSearch, setSourceSearch] = useState("")
  const [cityOptions, setCityOptions] = useState<CityOption[]>([])
  const [nearbyCityOptions, setNearbyCityOptions] = useState<CityOption[]>([])
  const [relevantCityOptions, setRelevantCityOptions] = useState<CityOption[]>([])
  const [sourceOptions, setSourceOptions] = useState<SourceOption[]>([])
  const [defaultSourceOptions, setDefaultSourceOptions] = useState<SourceOption[]>([])
  const [hasMoreThanFiveSources, setHasMoreThanFiveSources] = useState(false)
  const [cityLoading, setCityLoading] = useState(false)
  const [sourceLoading, setSourceLoading] = useState(false)
  const [locationStatus, setLocationStatus] = useState<"idle" | "loading" | "ready" | "denied" | "unavailable">("idle")

  useEffect(() => {
    if (tab !== "all") {
      return
    }

    if (!hasHydrated || !accessToken) {
      setSourceOptions([])
      setDefaultSourceOptions([])
      setHasMoreThanFiveSources(false)
      setSourceLoading(false)
      return
    }

    const abortController = new AbortController()

    const loadSources = async () => {
      setSourceLoading(true)

      try {
        const params = new URLSearchParams({ per_page: "25" })
        if (sourceSearch.trim()) {
          params.set("name", sourceSearch.trim())
        }
        const data = await fetchFilterOptions(
          `${apiBaseUrl}${API_ROUTES.sources.all}?${params.toString()}`,
          accessToken,
          abortController.signal
        )
        const results = Array.isArray(data.results) ? data.results : []

        if (sourceSearch.trim()) {
          setSourceOptions(results)
        } else {
          setHasMoreThanFiveSources(results.length > 5)
          const defaultOptions = results.slice(0, 5)
          setDefaultSourceOptions(defaultOptions)
          setSourceOptions(defaultOptions)
        }
      } catch (error) {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Failed to load search filter sources", error)
        }
      } finally {
        setSourceLoading(false)
      }
    }

    const timeoutId = window.setTimeout(() => {
      loadSources().catch((error) => {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Unhandled source load error", error)
        }
      })
    }, 250)

    return () => {
      window.clearTimeout(timeoutId)
      abortController.abort()
    }
  }, [accessToken, hasHydrated, sourceSearch, tab])

  useEffect(() => {
    if (tab !== "all") {
      return
    }

    if (!hasHydrated || !accessToken) {
      setRelevantCityOptions([])
      return
    }

    const abortController = new AbortController()

    const loadRelevantCities = async () => {
      try {
        const data = await fetchFilterOptions(
          `${apiBaseUrl}/locations/cities/relevant?per_page=5`,
          accessToken,
          abortController.signal
        )
        setRelevantCityOptions(Array.isArray(data.results) ? data.results : [])
      } catch (error) {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Failed to load relevant cities", error)
        }
      }
    }

    void loadRelevantCities()

    return () => {
      abortController.abort()
    }
  }, [accessToken, hasHydrated, tab])

  useEffect(() => {
    if (tab !== "all") {
      return
    }

    if (!hasHydrated || !accessToken) {
      setCityOptions([])
      setCityLoading(false)
      return
    }

    if (!citySearch.trim()) {
      setCityOptions([])
      return
    }

    const abortController = new AbortController()

    const loadCities = async () => {
      setCityLoading(true)

      try {
        const params = new URLSearchParams({
          term: citySearch.trim(),
          per_page: "25"
        })
        const data = await fetchFilterOptions(
          `${apiBaseUrl}/locations/cities?${params.toString()}`,
          accessToken,
          abortController.signal
        )
        setCityOptions(Array.isArray(data.results) ? data.results : [])
      } catch (error) {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Failed to load search filter locations", error)
        }
      } finally {
        setCityLoading(false)
      }
    }

    const timeoutId = window.setTimeout(() => {
      loadCities().catch((error) => {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Unhandled location load error", error)
        }
      })
    }, 250)

    return () => {
      window.clearTimeout(timeoutId)
      abortController.abort()
    }
  }, [accessToken, citySearch, hasHydrated, tab])

  useEffect(() => {
    if (tab !== "all" || !hasHydrated || !accessToken) {
      setNearbyCityOptions([])
      if (!hasHydrated || !accessToken) {
        setLocationStatus("idle")
      }
      return
    }

    if (typeof navigator === "undefined" || !navigator.geolocation) {
      setLocationStatus("unavailable")
      return
    }

    let cancelled = false

    const loadNearbyCities = async (latitude: number, longitude: number) => {
      setLocationStatus("loading")
      setCityLoading(true)

      try {
        const params = new URLSearchParams({
          latitude: String(latitude),
          longitude: String(longitude),
          per_page: "5"
        })
        const data = await fetchFilterOptions(
          `${apiBaseUrl}/locations/cities/nearby?${params.toString()}`,
          accessToken,
          new AbortController().signal
        )

        if (cancelled) {
          return
        }

        setNearbyCityOptions(Array.isArray(data.results) ? data.results : [])
        setLocationStatus("ready")
      } catch (error) {
        if (!cancelled) {
          console.error("Failed to load nearby cities", error)
          setLocationStatus("unavailable")
        }
      } finally {
        if (!cancelled) {
          setCityLoading(false)
        }
      }
    }

    const maybeAutoLocate = async () => {
      if (!("permissions" in navigator) || !navigator.permissions?.query) {
        return
      }

      try {
        const permissionStatus = await navigator.permissions.query({ name: "geolocation" })
        if (cancelled) {
          return
        }

        if (permissionStatus.state === "granted") {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              void loadNearbyCities(position.coords.latitude, position.coords.longitude)
            },
            () => {
              if (!cancelled) {
                setLocationStatus("denied")
              }
            },
            { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 }
          )
        } else if (permissionStatus.state === "denied") {
          setLocationStatus("denied")
        }
      } catch {
        // Ignore permission API failures and leave manual trigger available.
      }
    }

    void maybeAutoLocate()

    return () => {
      cancelled = true
    }
  }, [accessToken, hasHydrated, tab])

  const requestNearbyCities = async () => {
    if (!accessToken || typeof navigator === "undefined" || !navigator.geolocation) {
      setLocationStatus("unavailable")
      return
    }

    setLocationStatus("loading")

    navigator.geolocation.getCurrentPosition(
      async (position) => {
      try {
        setCityLoading(true)
        const params = new URLSearchParams({
          latitude: String(position.coords.latitude),
          longitude: String(position.coords.longitude),
            per_page: "5"
          })
          const data = await fetchFilterOptions(
            `${apiBaseUrl}/locations/cities/nearby?${params.toString()}`,
            accessToken,
            new AbortController().signal
          )
          setNearbyCityOptions(Array.isArray(data.results) ? data.results : [])
          setLocationStatus("ready")
        } catch (error) {
          console.error("Failed to load nearby cities", error)
          setLocationStatus("unavailable")
        } finally {
          setCityLoading(false)
        }
      },
      () => {
        setLocationStatus("denied")
        setCityLoading(false)
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 }
    )
  }

  const selectedCityItems = useMemo<FilterItem[]>(
    () =>
      city.map((label, index) => ({
        id: cityUid[index] ?? `selected-city-${label}`,
        title: label,
        checked: true,
        onToggle: () => {
          setFilters({
            city: city.filter((_, cityIndex) => cityIndex !== index),
            cityUid: cityUid.filter((_, cityIndex) => cityIndex !== index)
          })
        }
      })),
    [city, cityUid, setFilters]
  )

  const availableCityItems = useMemo<FilterItem[]>(
    () =>
      (citySearch.trim() ? cityOptions : nearbyCityOptions.length > 0 ? nearbyCityOptions : relevantCityOptions)
        .filter((option) => !cityUid.includes(option.uid))
        .map((option) => ({
          id: option.uid,
          title: formatCityLabel(option),
          checked: false,
          onToggle: () => {
            setFilters({
              city: [...city, formatCityLabel(option)],
              cityUid: [...cityUid, option.uid]
            })
          }
        })),
    [city, cityOptions, cityUid, nearbyCityOptions, relevantCityOptions, citySearch, setFilters]
  )

  const sourceItems = useMemo<FilterItem[]>(
    () =>
      [
        ...source.map((name, index) => ({
          id: sourceUid[index] ?? `selected-source-${name}`,
          title: name,
          checked: true,
          onToggle: () => {
            setFilters({
              source: source.filter((_, sourceIndex) => sourceIndex !== index),
              sourceUid: sourceUid.filter((_, sourceIndex) => sourceIndex !== index)
            })
          }
        })),
        ...sourceOptions
          .filter((option) => !sourceUid.includes(option.uid))
          .map((option) => ({
            id: option.uid,
            title: option.name,
            checked: false,
            onToggle: () => {
              setFilters({
                source: [...source, option.name],
                sourceUid: [...sourceUid, option.uid]
              })
            }
          }))
      ],
    [source, sourceOptions, sourceUid, setFilters]
  )

  const showSourceSearch = hasMoreThanFiveSources || sourceSearch.trim().length > 0
  const sourceFilters = showSourceSearch ? sourceItems : sourceItems.slice(0, 5)

  if (tab !== "all") {
    return (
      <section className={styles.filterWrapper}>
        <h3 className={styles.filterTitleText}>Filters</h3>
        <div className={styles.filterContentsWrapper}>
          <Typography variant="body2" color="text.secondary">
            Filters are currently available on the All tab.
          </Typography>
        </div>
      </section>
    )
  }

  return (
    <section className={styles.filterWrapper}>
      <h3 className={styles.filterTitleText}>Filters</h3>
      <div className={styles.filterContentsWrapper}>
        <FilterGroup
          withSearch
          filters={[...selectedCityItems, ...availableCityItems]}
          title="Location"
          searchValue={citySearch}
          onSearchChange={setCitySearch}
          loading={cityLoading}
          helperAction={
            !citySearch.trim() && locationStatus !== "ready" ? (
              <Button size="small" onClick={() => void requestNearbyCities()}>
                Use my location
              </Button>
            ) : null
          }
          helperText={
            !citySearch.trim() && locationStatus === "ready"
              ? "Nearby cities"
              : !citySearch.trim() && locationStatus === "denied"
                ? relevantCityOptions.length > 0
                  ? "Location access denied. Showing profile-based or data-rich cities."
                  : "Location access denied. Search manually instead."
              : !citySearch.trim() && relevantCityOptions.length > 0
                ? "Suggested from your profile or cities with rich data"
                : undefined
          }
        />
        <FilterGroup
          withSearch={showSourceSearch}
          filters={sourceFilters}
          title="Data Source"
          searchValue={sourceSearch}
          onSearchChange={setSourceSearch}
          loading={sourceLoading}
          searchPlaceholder="search data source..."
          emptyMessage="No matching sources"
        />
      </div>
    </section>
  )
}

type FilterGroupProps = {
  withSearch?: boolean
  filters: FilterItem[]
  title: string
  searchValue?: string
  onSearchChange?: (value: string) => void
  loading?: boolean
  searchPlaceholder?: string
  emptyMessage?: string
  helperAction?: ReactNode
  helperText?: string
}

const FilterGroup = ({
  withSearch = false,
  filters = [],
  title,
  searchValue = "",
  onSearchChange,
  loading = false,
  searchPlaceholder = "search city, state...",
  emptyMessage = "No matching results",
  helperAction,
  helperText
}: FilterGroupProps) => {
  return (
    <FormGroup sx={{ marginBottom: "1.5rem" }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBlockEnd: "0.5rem" }}>
        <Typography variant="subtitle1" sx={{ fontWeight: "600" }}>
          {title}
        </Typography>
        {helperAction}
      </Box>
      {helperText ? (
        <Typography variant="body2" color="text.secondary" sx={{ marginBlockEnd: "0.5rem" }}>
          {helperText}
        </Typography>
      ) : null}
      {withSearch && (
        <TextField
          id="search"
          variant="outlined"
          fullWidth
          value={searchValue}
          onChange={(event) => onSearchChange?.(event.target.value)}
          sx={{
            marginBottom: "1rem",
            "& .MuiInputBase-root": {
              height: "40px"
            }
          }}
          placeholder={searchPlaceholder}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
              endAdornment: loading ? <CircularProgress size={16} /> : undefined
            }
          }}
        />
      )}
      <Box
        sx={{
          maxHeight: withSearch ? 260 : 220,
          overflowY: "auto",
          pr: 0.5
        }}
      >
        {filters.map((filter) => (
          <Box
            key={filter.id}
            sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
          >
            <FormControlLabel
              control={<Checkbox checked={filter.checked} onChange={filter.onToggle} />}
              label={filter.title}
            />
          </Box>
        ))}
      </Box>
      {!withSearch && loading && <CircularProgress size={16} sx={{ mt: 1 }} />}
      {withSearch && filters.length === 0 && !loading && searchValue.trim() ? (
        <Typography variant="body2" color="text.secondary" className={styles.filterText}>
          {emptyMessage}
        </Typography>
      ) : null}
    </FormGroup>
  )
}

export default Filter
