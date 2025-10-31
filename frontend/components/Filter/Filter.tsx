import TextField from "@mui/material/TextField/TextField"
import styles from "./filter.module.css"
import {
  Checkbox,
  InputAdornment,
  FormGroup,
  Box,
  FormControlLabel,
  Typography,
  Stack,
  Chip
} from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useEffect, useState } from "react"
import { SearchParams } from "@/utils/api"

// TODO: Where should apply button go?
// TODO: Make show more do something
// TODO: Update to new design
// TODO: Handle dropdown for locations?

interface FilterData {
  title: string
  filter: string // key to use in API request
  options: Option[] // list of filtering options.
  withSearch?: boolean
}

interface FilterProps {
  filters: FilterData[]
}

interface FilterSectionProps extends FilterData {
  activeFilters: Set<string>
  onToggle: (value: string) => void
}

type Option = {
  id: string | number
  title: string
  count: number
}

const Filter = ({ filters }: FilterProps) => {
  const { searchAll, searchState } = useSearch()

  // Initialize set of filters for every group
  const [activeFilters, setActiveFilters] = useState<Record<string, Set<string>>>(() => {
    const init: Record<string, Set<string>> = {}
    filters.forEach((f) => {
      init[f.filter] = new Set()
    })
    return init
  })

  // Sync filters with searchState when it changes (or on first mount)
  useEffect(() => {
    if (!searchState) return

    setActiveFilters(() => {
      const updated: Record<string, Set<string>> = {}

      filters.forEach((f) => {
        const stateValues = searchState[f.filter]

        // If the current search state has this filter, reflect it
        if (Array.isArray(stateValues)) {
          updated[f.filter] = new Set(stateValues)
        } else if (typeof stateValues === "string") {
          updated[f.filter] = new Set([stateValues])
        } else {
          updated[f.filter] = new Set()
        }
      })

      return updated
    })
  }, [searchState, filters])

  // Toggle a value for a specific group
  const handleToggle = (filter: string, value: string) => {
    setActiveFilters((prev) => {
      const newOptions = { ...prev }
      // Add or remove the option
      const toggled = new Set(prev[filter])
      if (toggled.has(value)) {
        toggled.delete(value)
      } else {
        toggled.add(value)
      }
      newOptions[filter] = toggled

      return newOptions
    })
  }

  // Apply all active filters
  const applyFilters = async () => {
    const apiFilters: Record<string, string[]> = {}
    Object.entries(activeFilters).forEach(([key, set]) => {
      apiFilters[key] = [...set] // convert set to array
    })
    if (searchState) {
      const request: SearchParams = { ...searchState, ...apiFilters } // add filters to search state
      await searchAll(request)
    }
  }

  // Clear all filters
  const clearFilters = async () => {
    const cleared: Record<string, Set<string>> = {}
    filters.forEach((f) => {
      cleared[f.filter] = new Set()
    })

    setActiveFilters(cleared)
    if (searchState) {
      // Construct an empty filter object (no filters applied) and redo search
      const request: SearchParams = { ...searchState }
      filters.forEach((f) => {
        delete request[f.filter]
      })
      await searchAll(request)
    }
  }
  return (
    <section className={styles.filterWrapper}>
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        spacing={1.5}
        sx={{ marginTop: "1rem", marginBottom: "1rem" }}
      >
        <h3 className={styles.filterTitleText}>Filters</h3>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Chip
            label="Apply"
            color="default"
            size="small"
            variant="filled"
            onClick={applyFilters}
            sx={{
              borderRadius: "100px",
              backgroundColor: "#00000014",
              fontWeight: 500,
              "&:hover": {
                backgroundColor: "#00000025"
              }
            }}
          />
          <Chip
            label="Clear"
            color="default"
            size="small"
            variant="filled"
            onClick={clearFilters}
            sx={{
              borderRadius: "100px",
              backgroundColor: "#00000014",
              fontWeight: 500,
              "&:hover": {
                backgroundColor: "#00000025"
              }
            }}
          />
        </Box>
      </Stack>
      <div className={styles.filterContentsWrapper}>
        {filters.map((f) => (
          <FilterSection
            key={f.filter}
            {...f}
            activeFilters={activeFilters[f.filter]}
            onToggle={(option: string) => handleToggle(f.filter, option)}
          />
        ))}
      </div>
    </section>
  )
}

const FilterSection = ({
  title,
  filter,
  options,
  activeFilters,
  onToggle,
  withSearch = false
}: FilterSectionProps) => {
  return (
    <FormGroup sx={{ marginBottom: "1.5rem" }}>
      <Typography variant="subtitle1" sx={{ marginBlockEnd: "0.5rem", fontWeight: "600" }}>
        {title}
      </Typography>
      {withSearch && (
        <TextField
          id={`${filter}-search`}
          variant="outlined"
          fullWidth
          placeholder="search city, state..."
          sx={{
            marginBottom: "1rem",
            "& .MuiInputBase-root": { height: "40px" }
          }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <Search fontSize="small" />
                </InputAdornment>
              )
            }
          }}
        />
      )}
      {options.map((option) => (
        <Box
          key={option.id}
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "0.25rem"
          }}
        >
          <FormControlLabel
            control={
              <Checkbox
                checked={activeFilters.has(option.title)}
                onChange={() => onToggle(option.title)}
                size="small"
              />
            }
            label={option.title}
          />
          <Typography variant="body2" color="text.secondary">
            {option.count}
          </Typography>
        </Box>
      ))}
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ cursor: "pointer", marginTop: "0.5rem" }}
      >
        Show more...
      </Typography>
    </FormGroup>
  )
}

export default Filter
