"use client"

import { useEffect, useMemo, useState } from "react"
import TextField from "@mui/material/TextField"
import styles from "./filter.module.css"
import {
  Checkbox,
  CircularProgress,
  InputAdornment,
  FormGroup,
  Box,
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
  const [sourceOptions, setSourceOptions] = useState<SourceOption[]>([])
  const [defaultSourceOptions, setDefaultSourceOptions] = useState<SourceOption[]>([])
  const [hasMoreThanFiveSources, setHasMoreThanFiveSources] = useState(false)
  const [cityLoading, setCityLoading] = useState(false)
  const [sourceLoading, setSourceLoading] = useState(false)

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
      cityOptions
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
    [city, cityOptions, cityUid, setFilters]
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
}

const FilterGroup = ({
  withSearch = false,
  filters = [],
  title,
  searchValue = "",
  onSearchChange,
  loading = false,
  searchPlaceholder = "search city, state...",
  emptyMessage = "No matching results"
}: FilterGroupProps) => {
  return (
    <FormGroup sx={{ marginBottom: "1.5rem" }}>
      <Typography variant="subtitle1" sx={{ marginBlockEnd: "0.5rem", fontWeight: "600" }}>
        {title}
      </Typography>
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
