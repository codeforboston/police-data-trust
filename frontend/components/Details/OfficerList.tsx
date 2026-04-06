"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import {
  Box,
  Checkbox,
  Chip,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  TextField,
  InputAdornment,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  CircularProgress
} from "@mui/material"
import type { SelectChangeEvent } from "@mui/material/Select"
import ListItemText from "@mui/material/ListItemText"
import { Search, TableRows, Apps } from "@mui/icons-material"
import { Officer, HasOfficers } from "@/utils/api"
import DetailCard from "@/components/Details/DetailCard"
import {
  DEFAULT_OFFICER_LIST_FILTERS,
  mergeOfficerListFilters,
  OfficerListFilters,
  useOfficerListFilters
} from "@/hooks/useOfficerListFilters"
import {
  EMPLOYMENT_TYPE_OPTIONS,
  EMPLOYMENT_RANK_OPTIONS,
  EMPLOYMENT_STATUS_OPTIONS,
  formatEmploymentOptionLabel
} from "@/utils/employmentOptions"

type OfficerListFilterMode = "client" | "hybrid"

type OfficerListProps = {
  org: HasOfficers
  orgType: "agency" | "unit"
  officers?: Officer[]
  activeOfficerCount?: number
  inactiveOfficerCount?: number
  loading?: boolean
  error?: Error | null
  filters?: OfficerListFilters
  onFiltersChange?: (filters: OfficerListFilters) => void
  filterMode?: OfficerListFilterMode
}

export default function OfficerList({
  org,
  orgType,
  officers = [],
  activeOfficerCount,
  inactiveOfficerCount,
  loading = false,
  error = null,
  filters,
  onFiltersChange,
  filterMode = "client"
}: OfficerListProps) {
  const router = useRouter()
  const [viewMode, setViewMode] = React.useState<"card" | "table">("table")
  const { filters: internalFilters, setFilters: setInternalFilters } = useOfficerListFilters(
    DEFAULT_OFFICER_LIST_FILTERS
  )
  const showUnitColumn = orgType === "agency"
  const currentFilters = filters ?? internalFilters

  const updateFilters = React.useCallback(
    (updates: Partial<OfficerListFilters>) => {
      const nextFilters = mergeOfficerListFilters(currentFilters, updates)

      if (!filters) {
        setInternalFilters(nextFilters)
      }

      onFiltersChange?.(nextFilters)
    },
    [currentFilters, filters, onFiltersChange, setInternalFilters]
  )

  const handleViewModeChange = (
    _event: React.MouseEvent<HTMLElement>,
    newMode: "card" | "table" | null
  ) => {
    if (newMode) setViewMode(newMode)
  }

  const activeCount = activeOfficerCount ?? org.total_officers ?? 0
  const inactiveCount = inactiveOfficerCount ?? 0

  const handleMultiSelectChange = React.useCallback(
    (key: "status" | "rank" | "type" | "unit") => (event: SelectChangeEvent<string[]>) => {
      const value = event.target.value
      updateFilters({
        [key]: typeof value === "string" ? value.split(",") : value
      } as Pick<OfficerListFilters, typeof key>)
    },
    [updateFilters]
  )

  const renderMultiSelectValue = React.useCallback((selected: string[]) => {
    if (selected.length === 0) {
      return "All"
    }

    return (
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
        {selected.map((value) => (
          <Chip
            key={value}
            label={value.includes("_") ? formatEmploymentOptionLabel(value) : value}
            size="small"
            sx={{ maxWidth: "100%" }}
          />
        ))}
      </Box>
    )
  }, [])

  const rankOptions = React.useMemo(() => [...EMPLOYMENT_RANK_OPTIONS], [])

  const typeOptions = React.useMemo(() => [...EMPLOYMENT_TYPE_OPTIONS], [])

  const statusOptions = React.useMemo(() => [...EMPLOYMENT_STATUS_OPTIONS], [])

  const uniqueUnits = React.useMemo(() => {
    const units = new Set<string>()
    officers.forEach((officer) => {
      if (officer.employment?.unit?.name) {
        units.add(officer.employment.unit.name)
      }
    })
    currentFilters.unit.forEach((unit) => units.add(unit))
    return Array.from(units).sort()
  }, [currentFilters.unit, officers])

  const filtered = officers.filter((officer) => {
    const name =
      `${officer.first_name} ${officer.middle_name || ""} ${officer.last_name}`.toLowerCase()
    const matchesSearch =
      filterMode === "hybrid" ||
      currentFilters.searchTerm.trim() === "" ||
      name.includes(currentFilters.searchTerm.toLowerCase())

    const status = officer.employment?.status
    const matchesStatus =
      filterMode === "hybrid" ||
      currentFilters.status.length === 0 ||
      currentFilters.status.includes(status ?? "")

    const matchesRank =
      filterMode === "hybrid" ||
      currentFilters.rank.length === 0 ||
      currentFilters.rank.includes(officer.employment?.rank ?? "")
    const matchesType =
      filterMode === "hybrid" ||
      currentFilters.type.length === 0 ||
      currentFilters.type.includes(officer.employment?.type ?? "")
    const matchesUnit =
      currentFilters.unit.length === 0 ||
      currentFilters.unit.includes(officer.employment?.unit?.name ?? "")

    return matchesSearch && matchesStatus && matchesRank && matchesType && matchesUnit
  })

  return (
    <Box>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2, alignItems: "center" }}>
        <Box sx={{ flexGrow: 1, minWidth: 240 }}>
          <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: 500 }}>
            Officers list
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary", mt: 0.5 }}>
            {activeCount} active officers · {inactiveCount} inactive officers
          </Typography>
        </Box>

        <ToggleButtonGroup
          value={viewMode}
          exclusive
          onChange={handleViewModeChange}
          size="small"
          sx={{ borderRadius: "999px", height: 40 }}
        >
          <ToggleButton value="card" aria-label="card view">
            <Apps sx={{ mr: 1 }} />
            Card view
          </ToggleButton>
          <ToggleButton value="table" aria-label="table view">
            <TableRows sx={{ mr: 1 }} />
            Table view
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          gap: 2,
          alignItems: "center",
          mt: 3
        }}
      >
        <TextField
          variant="outlined"
          placeholder="search officer or try anything"
          value={currentFilters.searchTerm}
          onChange={(e) => updateFilters({ searchTerm: e.target.value })}
          sx={{ minWidth: 240, flex: 1, maxWidth: 500 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              )
            }
          }}
        />

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Status</InputLabel>
          <Select
            multiple
            label="Status"
            value={currentFilters.status}
            onChange={handleMultiSelectChange("status")}
            renderValue={(selected) => renderMultiSelectValue(selected)}
          >
            {statusOptions.map((status) => (
              <MenuItem key={status} value={status}>
                <Checkbox checked={currentFilters.status.includes(status)} />
                <ListItemText primary={formatEmploymentOptionLabel(status)} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Rank</InputLabel>
          <Select
            multiple
            label="Rank"
            value={currentFilters.rank}
            onChange={handleMultiSelectChange("rank")}
            renderValue={(selected) => renderMultiSelectValue(selected)}
          >
            {rankOptions.map((rank) => (
              <MenuItem key={rank} value={rank}>
                <Checkbox checked={currentFilters.rank.includes(rank)} />
                <ListItemText primary={rank} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 180 }} size="small">
          <InputLabel>Type</InputLabel>
          <Select
            multiple
            label="Type"
            value={currentFilters.type}
            onChange={handleMultiSelectChange("type")}
            renderValue={(selected) => renderMultiSelectValue(selected)}
          >
            {typeOptions.map((type) => (
              <MenuItem key={type} value={type}>
                <Checkbox checked={currentFilters.type.includes(type)} />
                <ListItemText primary={formatEmploymentOptionLabel(type)} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {showUnitColumn && (
          <FormControl sx={{ minWidth: 160 }} size="small">
            <InputLabel>Unit</InputLabel>
            <Select
              multiple
              label="Unit"
              value={currentFilters.unit}
              onChange={handleMultiSelectChange("unit")}
              renderValue={(selected) => renderMultiSelectValue(selected)}
            >
              {uniqueUnits.map((unit_name) => (
                <MenuItem key={unit_name} value={unit_name}>
                  <Checkbox checked={currentFilters.unit.includes(unit_name)} />
                  <ListItemText primary={unit_name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}
      </Box>

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" sx={{ mt: 3 }}>
          Could not load officers.
        </Typography>
      ) : viewMode === "table" ? (
        <Paper sx={{ width: "100%", mt: 3, overflowX: "auto" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Officer name</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Badge ID</TableCell>
                <TableCell>Rank</TableCell>
                <TableCell>Type</TableCell>
                {showUnitColumn && <TableCell>Unit</TableCell>}
                <TableCell>Years of service</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.length > 0 ? (
                filtered.map((officer) => (
                  <TableRow
                    key={officer.uid}
                    hover
                    onClick={() => router.push(`/officer/${officer.uid}`)}
                    sx={{
                      cursor: "pointer",
                      "&:hover": { backgroundColor: "action.hover" }
                    }}
                  >
                    <TableCell>
                      {officer.first_name} {officer.middle_name} {officer.last_name}
                    </TableCell>
                    <TableCell>
                      {officer.employment?.status
                        ? formatEmploymentOptionLabel(officer.employment.status)
                        : "Unknown"}
                    </TableCell>
                    <TableCell>{officer.employment?.badge_number}</TableCell>
                    <TableCell>{officer.employment?.rank}</TableCell>
                    <TableCell>
                      {officer.employment?.type
                        ? formatEmploymentOptionLabel(officer.employment.type)
                        : "Unknown"}
                    </TableCell>
                    {showUnitColumn && <TableCell>{officer.employment?.unit?.name}</TableCell>}
                    <TableCell>
                      {officer.employment?.earliest_date} –{" "}
                      {officer.employment?.latest_date ?? "Current"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={showUnitColumn ? 7 : 6} sx={{ textAlign: "center", py: 4 }}>
                    No officers found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Paper>
      ) : (
        <DetailCard sx={{ mt: 3 }}>
          <Typography sx={{ py: 4, textAlign: "center", color: "text.disabled" }}>
            Card view is temporarily unavailable
          </Typography>
        </DetailCard>
      )}
    </Box>
  )
}
