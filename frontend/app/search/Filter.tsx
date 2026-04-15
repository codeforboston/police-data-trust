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
import { ExpandLess, ExpandMore, Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useAuth } from "@/providers/AuthProvider"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { US_STATES } from "@/utils/constants"

type CityOption = {
  uid: string
  name: string
  state?: {
    abbreviation?: string
    name?: string
  }
}

type StateOption = {
  uid: string
  name: string
  abbreviation: string
}

type SourceOption = {
  uid: string
  name: string
}

type JurisdictionOption = {
  value: string
  label: string
}

type FilterItem = {
  id: string
  title: string
  checked: boolean
  onToggle: () => void
}

type LocationStateGroup = {
  id: string
  name: string
  abbreviation: string
  cities: CityOption[]
}

const formatCityLabel = (city: CityOption) =>
  city.state?.abbreviation ? `${city.name}, ${city.state.abbreviation}` : city.name

const JURISDICTION_OPTIONS: JurisdictionOption[] = [
  { value: "FEDERAL", label: "Federal" },
  { value: "STATE", label: "State" },
  { value: "COUNTY", label: "County" },
  { value: "MUNICIPAL", label: "Municipal" },
  { value: "PRIVATE", label: "Private" },
  { value: "OTHER", label: "Other" }
]

const parseCityLabel = (label: string) => {
  const parts = label.split(",").map((part) => part.trim())
  if (parts.length >= 2) {
    return {
      name: parts.slice(0, -1).join(", "),
      stateAbbreviation: parts[parts.length - 1]
    }
  }

  return { name: label, stateAbbreviation: undefined }
}

const normalizeLocationSearchTerm = (value: string) => value.trim().replace(/\s+/g, " ")

const findStateAbbreviation = (value: string) => {
  const normalized = normalizeLocationSearchTerm(value).toLowerCase()
  const match = US_STATES.find(
    (stateOption) =>
      stateOption.abbreviation.toLowerCase() === normalized ||
      stateOption.name.toLowerCase() === normalized
  )

  return match?.abbreviation
}

const parseLocationSearch = (value: string) => {
  const normalized = normalizeLocationSearchTerm(value)
  if (!normalized) {
    return { cityTerm: "", stateAbbreviation: undefined as string | undefined, stateSearchTerm: "" }
  }

  const commaParts = normalized.split(",").map((part) => part.trim()).filter(Boolean)
  if (commaParts.length >= 2) {
    const stateAbbreviation = findStateAbbreviation(commaParts[commaParts.length - 1])
    if (stateAbbreviation) {
      return {
        cityTerm: commaParts.slice(0, -1).join(", "),
        stateAbbreviation,
        stateSearchTerm: commaParts[commaParts.length - 1]
      }
    }
  }

  for (const stateOption of US_STATES) {
    const stateName = stateOption.name.toLowerCase()
    const stateAbbreviation = stateOption.abbreviation.toLowerCase()
    const lowered = normalized.toLowerCase()

    if (lowered.endsWith(` ${stateName}`)) {
      return {
        cityTerm: normalized.slice(0, normalized.length - stateOption.name.length).trim().replace(/,$/, "").trim(),
        stateAbbreviation: stateOption.abbreviation,
        stateSearchTerm: stateOption.name
      }
    }

    if (lowered.endsWith(` ${stateAbbreviation}`)) {
      return {
        cityTerm: normalized.slice(0, normalized.length - stateOption.abbreviation.length).trim().replace(/,$/, "").trim(),
        stateAbbreviation: stateOption.abbreviation,
        stateSearchTerm: stateOption.abbreviation
      }
    }
  }

  return { cityTerm: normalized, stateAbbreviation: undefined as string | undefined, stateSearchTerm: normalized }
}

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
    state: { tab, state, city, cityUid, source, sourceUid, jurisdiction },
    setFilters
  } = useSearch()
  const { accessToken, hasHydrated } = useAuth()
  const [locationSearch, setLocationSearch] = useState("")
  const [searchedCities, setSearchedCities] = useState<CityOption[]>([])
  const [searchedStates, setSearchedStates] = useState<StateOption[]>([])
  const [nearbyCityOptions, setNearbyCityOptions] = useState<CityOption[]>([])
  const [relevantCityOptions, setRelevantCityOptions] = useState<CityOption[]>([])
  const [sourceSearch, setSourceSearch] = useState("")
  const [sourceOptions, setSourceOptions] = useState<SourceOption[]>([])
  const [hasMoreThanFiveSources, setHasMoreThanFiveSources] = useState(false)
  const [locationLoading, setLocationLoading] = useState(false)
  const [sourceLoading, setSourceLoading] = useState(false)
  const [locationStatus, setLocationStatus] = useState<
    "idle" | "loading" | "ready" | "denied" | "unavailable"
  >("idle")

  useEffect(() => {
    if (tab !== "all" && tab !== "agencies") {
      return
    }

    if (!hasHydrated || !accessToken) {
      setSourceOptions([])
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

        setHasMoreThanFiveSources(results.length > 5)
        setSourceOptions(sourceSearch.trim() ? results : results.slice(0, 5))
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
    if (tab !== "all" && tab !== "agencies") {
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
    if (tab !== "all" && tab !== "agencies") {
      return
    }

    if (!hasHydrated || !accessToken) {
      setSearchedCities([])
      setSearchedStates([])
      setLocationLoading(false)
      return
    }

    if (!locationSearch.trim()) {
      setSearchedCities([])
      setSearchedStates([])
      setLocationLoading(false)
      return
    }

    const abortController = new AbortController()

    const loadLocationSuggestions = async () => {
      setLocationLoading(true)

      try {
        const parsedSearch = parseLocationSearch(locationSearch)
        const cityParams = new URLSearchParams({
          term: parsedSearch.cityTerm || normalizeLocationSearchTerm(locationSearch),
          per_page: "20"
        })
        if (parsedSearch.stateAbbreviation) {
          cityParams.set("state", parsedSearch.stateAbbreviation)
        }
        const stateParams = new URLSearchParams({
          term: parsedSearch.stateSearchTerm || normalizeLocationSearchTerm(locationSearch),
          per_page: "10"
        })

        const [cityData, stateData] = await Promise.all([
          fetchFilterOptions(
            `${apiBaseUrl}/locations/cities?${cityParams.toString()}`,
            accessToken,
            abortController.signal
          ),
          fetchFilterOptions(
            `${apiBaseUrl}/locations/states?${stateParams.toString()}`,
            accessToken,
            abortController.signal
          )
        ])

        setSearchedCities(Array.isArray(cityData.results) ? cityData.results : [])
        setSearchedStates(Array.isArray(stateData.results) ? stateData.results : [])
      } catch (error) {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Failed to load location suggestions", error)
        }
      } finally {
        setLocationLoading(false)
      }
    }

    const timeoutId = window.setTimeout(() => {
      loadLocationSuggestions().catch((error) => {
        if (!isBenignFilterFetchError(error, abortController.signal)) {
          console.error("Unhandled location suggestion error", error)
        }
      })
    }, 250)

    return () => {
      window.clearTimeout(timeoutId)
      abortController.abort()
    }
  }, [accessToken, hasHydrated, locationSearch, tab])

  useEffect(() => {
    if ((tab !== "all" && tab !== "agencies") || !hasHydrated || !accessToken) {
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
      setLocationLoading(true)

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
          setLocationLoading(false)
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
        // keep manual trigger available
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
    setLocationLoading(true)

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
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
          setLocationLoading(false)
        }
      },
      () => {
        setLocationStatus("denied")
        setLocationLoading(false)
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 }
    )
  }

  const sourceItems = useMemo<FilterItem[]>(
    () => [
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
  const jurisdictionItems = useMemo<FilterItem[]>(
    () =>
      JURISDICTION_OPTIONS.map((option) => ({
        id: option.value,
        title: option.label,
        checked: jurisdiction.includes(option.value),
        onToggle: () => {
          if (jurisdiction.includes(option.value)) {
            setFilters({
              jurisdiction: jurisdiction.filter((value) => value !== option.value)
            })
            return
          }

          setFilters({
            jurisdiction: [...jurisdiction, option.value]
          })
        }
      })),
    [jurisdiction, setFilters]
  )

  if (tab !== "all" && tab !== "agencies") {
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
        <LocationFilterGroup
          loading={locationLoading}
          searchValue={locationSearch}
          onSearchChange={setLocationSearch}
          selectedStates={state}
          selectedCities={city}
          selectedCityUids={cityUid}
          searchedStates={searchedStates}
          searchedCities={searchedCities}
          nearbyCities={nearbyCityOptions}
          relevantCities={relevantCityOptions}
          locationStatus={locationStatus}
          onRequestNearbyCities={requestNearbyCities}
          onFiltersChange={setFilters}
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
        {tab === "agencies" ? (
          <FilterGroup
            filters={jurisdictionItems}
            title="Jurisdiction"
            helperText="Filter agencies by jurisdiction type"
          />
        ) : null}
      </div>
    </section>
  )
}

type LocationFilterGroupProps = {
  loading: boolean
  searchValue: string
  onSearchChange: (value: string) => void
  selectedStates: string[]
  selectedCities: string[]
  selectedCityUids: string[]
  searchedStates: StateOption[]
  searchedCities: CityOption[]
  nearbyCities: CityOption[]
  relevantCities: CityOption[]
  locationStatus: "idle" | "loading" | "ready" | "denied" | "unavailable"
  onRequestNearbyCities: () => void | Promise<void>
  onFiltersChange: (filters: {
    state?: string[]
    city?: string[]
    cityUid?: string[]
  }) => void
}

const LocationFilterGroup = ({
  loading,
  searchValue,
  onSearchChange,
  selectedStates,
  selectedCities,
  selectedCityUids,
  searchedStates,
  searchedCities,
  nearbyCities,
  relevantCities,
  locationStatus,
  onRequestNearbyCities,
  onFiltersChange
}: LocationFilterGroupProps) => {
  const [expandedStates, setExpandedStates] = useState<Record<string, boolean>>({})

  const baseCities = searchValue.trim()
    ? searchedCities
    : nearbyCities.length > 0
      ? nearbyCities
      : relevantCities

  const locationGroups = useMemo<LocationStateGroup[]>(() => {
    const stateMap = new Map<string, LocationStateGroup>()

    const ensureState = (
      abbreviation: string,
      name?: string,
      id?: string
    ): LocationStateGroup => {
      const existing = stateMap.get(abbreviation)
      if (existing) {
        if (name && existing.name === abbreviation) {
          existing.name = name
        }
        return existing
      }

      const nextState: LocationStateGroup = {
        id: id ?? abbreviation,
        name: name ?? abbreviation,
        abbreviation,
        cities: []
      }
      stateMap.set(abbreviation, nextState)
      return nextState
    }

    searchedStates.forEach((stateOption) => {
      ensureState(stateOption.abbreviation, stateOption.name, stateOption.uid)
    })

    baseCities.forEach((cityOption) => {
      const abbreviation = cityOption.state?.abbreviation
      if (!abbreviation) {
        return
      }

      const group = ensureState(abbreviation, cityOption.state?.name)
      if (!group.cities.some((existingCity) => existingCity.uid === cityOption.uid)) {
        group.cities.push(cityOption)
      }
    })

    selectedStates.forEach((abbreviation) => {
      ensureState(abbreviation)
    })

    selectedCities.forEach((label, index) => {
      const parsed = parseCityLabel(label)
      if (!parsed.stateAbbreviation) {
        return
      }

      const group = ensureState(parsed.stateAbbreviation)
      if (!group.cities.some((existingCity) => existingCity.uid === selectedCityUids[index])) {
        group.cities.push({
          uid: selectedCityUids[index],
          name: parsed.name,
          state: {
            abbreviation: parsed.stateAbbreviation
          }
        })
      }
    })

    return Array.from(stateMap.values())
      .map((group) => ({
        ...group,
        cities: [...group.cities].sort((left, right) => left.name.localeCompare(right.name))
      }))
      .sort((left, right) => left.name.localeCompare(right.name))
  }, [baseCities, searchedStates, selectedStates, selectedCities, selectedCityUids])

  useEffect(() => {
    if (!searchValue.trim()) {
      return
    }

    setExpandedStates((current) => {
      const nextState = { ...current }
      locationGroups.forEach((group) => {
        nextState[group.abbreviation] = true
      })
      return nextState
    })
  }, [locationGroups, searchValue])

  const toggleExpanded = (abbreviation: string) => {
    setExpandedStates((current) => ({
      ...current,
      [abbreviation]: !current[abbreviation]
    }))
  }

  const toggleState = (group: LocationStateGroup) => {
    const isSelected = selectedStates.includes(group.abbreviation)

    if (isSelected) {
      onFiltersChange({
        state: selectedStates.filter((value) => value !== group.abbreviation)
      })
      return
    }

    const cityIndexesForState = selectedCities
      .map((label, index) => ({ parsed: parseCityLabel(label), index }))
      .filter(({ parsed }) => parsed.stateAbbreviation === group.abbreviation)
      .map(({ index }) => index)

    onFiltersChange({
      state: [...selectedStates, group.abbreviation],
      city: selectedCities.filter((_, index) => !cityIndexesForState.includes(index)),
      cityUid: selectedCityUids.filter((_, index) => !cityIndexesForState.includes(index))
    })
  }

  const toggleCity = (cityOption: CityOption) => {
    const stateAbbreviation = cityOption.state?.abbreviation
    if (!stateAbbreviation || selectedStates.includes(stateAbbreviation)) {
      return
    }

    const existingIndex = selectedCityUids.indexOf(cityOption.uid)
    if (existingIndex >= 0) {
      onFiltersChange({
        city: selectedCities.filter((_, index) => index !== existingIndex),
        cityUid: selectedCityUids.filter((_, index) => index !== existingIndex)
      })
      return
    }

    onFiltersChange({
      city: [...selectedCities, formatCityLabel(cityOption)],
      cityUid: [...selectedCityUids, cityOption.uid]
    })
  }

  const helperText =
    !searchValue.trim() && locationStatus === "ready"
      ? "Nearby cities grouped by state"
      : !searchValue.trim() && locationStatus === "denied"
        ? relevantCities.length > 0
          ? "Location access denied. Showing profile-based or data-rich cities."
          : "Location access denied. Search manually instead."
        : !searchValue.trim() && relevantCities.length > 0
          ? "Suggested from your profile or cities with rich data"
          : undefined

  return (
    <FormGroup sx={{ marginBottom: "1.5rem" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBlockEnd: "0.5rem"
        }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: "600" }}>
          Location
        </Typography>
        {!searchValue.trim() && locationStatus !== "ready" ? (
          <Button size="small" onClick={() => void onRequestNearbyCities()}>
            Use my location
          </Button>
        ) : null}
      </Box>
      {helperText ? (
        <Typography variant="body2" color="text.secondary" sx={{ marginBlockEnd: "0.5rem" }}>
          {helperText}
        </Typography>
      ) : null}
      <TextField
        id="location-search"
        variant="outlined"
        fullWidth
        value={searchValue}
        onChange={(event) => onSearchChange(event.target.value)}
        sx={{
          marginBottom: "1rem",
          "& .MuiInputBase-root": {
            height: "40px"
          }
        }}
        placeholder="search city or state..."
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
      <Box
        sx={{
          maxHeight: 320,
          overflowY: "auto",
          pr: 0.5
        }}
      >
        {locationGroups.map((group) => {
          const isStateSelected = selectedStates.includes(group.abbreviation)
          const selectedChildCount = group.cities.filter((cityOption) =>
            selectedCityUids.includes(cityOption.uid)
          ).length
          const isIndeterminate = !isStateSelected && selectedChildCount > 0
          const isExpanded =
            expandedStates[group.abbreviation] ??
            (Boolean(searchValue.trim()) || isStateSelected || isIndeterminate)

          return (
            <Box key={group.id} sx={{ marginBottom: "0.25rem" }}>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Button
                  size="small"
                  sx={{ minWidth: 0, padding: "0.25rem", marginRight: "0.25rem" }}
                  onClick={() => toggleExpanded(group.abbreviation)}
                >
                  {isExpanded ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
                </Button>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={isStateSelected}
                      indeterminate={isIndeterminate}
                      onChange={() => toggleState(group)}
                    />
                  }
                  label={`${group.name}${group.name === group.abbreviation ? "" : ` (${group.abbreviation})`}`}
                />
              </Box>
              {isExpanded ? (
                <Box sx={{ marginLeft: "2rem" }}>
                  {group.cities.map((cityOption) => {
                    const parentSelected = selectedStates.includes(
                      cityOption.state?.abbreviation ?? ""
                    )
                    const cityChecked = parentSelected || selectedCityUids.includes(cityOption.uid)

                    return (
                      <Box key={cityOption.uid}>
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={cityChecked}
                              disabled={parentSelected}
                              onChange={() => toggleCity(cityOption)}
                            />
                          }
                          label={cityOption.name}
                        />
                      </Box>
                    )
                  })}
                </Box>
              ) : null}
            </Box>
          )
        })}
      </Box>
      {locationGroups.length === 0 && !loading && searchValue.trim() ? (
        <Typography variant="body2" color="text.secondary" className={styles.filterText}>
          No matching locations
        </Typography>
      ) : null}
    </FormGroup>
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
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBlockEnd: "0.5rem"
        }}
      >
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
          id={`${title.toLowerCase()}-search`}
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
