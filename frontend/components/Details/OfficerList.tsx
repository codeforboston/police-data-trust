"use client"

import * as React from "react"
import {
  Box,
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
import { Search, TableRows, Apps } from "@mui/icons-material"
import { Officer, Unit } from "@/utils/api"
import OfficerListItem from "@/components/officer/OfficerListItem"
import DetailCard from "@/components/Details/DetailCard"

type OfficerListProps = {
  unit: Unit
  officers?: Officer[]
  activeOfficerCount?: number
  inactiveOfficerCount?: number
  loading?: boolean
  error?: Error | null
}

export default function OfficerList({
  unit,
  officers = [],
  activeOfficerCount,
  inactiveOfficerCount,
  loading = false,
  error = null
}: OfficerListProps) {
  const [viewMode, setViewMode] = React.useState<"card" | "table">("table")
  const [searchValue, setSearchValue] = React.useState("")
  const [statusFilter, setStatusFilter] = React.useState<string>("all")
  const [rankFilter, setRankFilter] = React.useState<string>("all")
  const [unitFilter, setUnitFilter] = React.useState<string>("all")

  const handleViewModeChange = (
    _event: React.MouseEvent<HTMLElement>,
    newMode: "card" | "table" | null
  ) => {
    if (newMode) setViewMode(newMode)
  }

  const activeCount = activeOfficerCount ?? unit.total_officers ?? 0
  const inactiveCount = inactiveOfficerCount ?? 0

  // Extract unique values for filter dropdowns
  const uniqueStatuses = React.useMemo(() => {
    const statuses = new Set<string>()
    officers.forEach((officer) => {
      const status = officer.employment?.latest_date ? "Inactive" : "Active"
      statuses.add(status)
    })
    return Array.from(statuses).sort()
  }, [officers])

  const uniqueRanks = React.useMemo(() => {
    const ranks = new Set<string>()
    officers.forEach((officer) => {
      if (officer.employment?.rank) {
        ranks.add(officer.employment.rank)
      }
    })
    return Array.from(ranks).sort()
  }, [officers])

  const uniqueUnits = React.useMemo(() => {
    const units = new Set<string>()
    officers.forEach((officer) => {
      if (officer.employment?.unit?.name) {
        units.add(officer.employment.unit.name)
      }
    })
    return Array.from(units).sort()
  }, [officers])

  const filtered = officers.filter((officer) => {
    const name =
      `${officer.first_name} ${officer.middle_name || ""} ${officer.last_name}`.toLowerCase()
    const matchesSearch = searchValue.trim() === "" || name.includes(searchValue.toLowerCase())

    const status = officer.employment?.latest_date ? "Inactive" : "Active"
    const matchesStatus = statusFilter === "all" || statusFilter === status

    const matchesRank = rankFilter === "all" || rankFilter === officer.employment?.rank
    const matchesUnit = unitFilter === "all" || unitFilter === officer.employment?.unit?.name

    return matchesSearch && matchesStatus && matchesRank && matchesUnit
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
          sx={{ borderRadius: "999px", height: 40 }}>
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
        }}>
        <TextField
          variant="outlined"
          placeholder="search officer or try anything"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
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
            label="Status"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}>
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="Active">Active</MenuItem>
            <MenuItem value="Inactive">Inactive</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Rank</InputLabel>
          <Select label="Rank" value={rankFilter} onChange={(e) => setRankFilter(e.target.value)}>
            <MenuItem value="all">All</MenuItem>
            {uniqueRanks.map((rank) => (
              <MenuItem key={rank} value={rank}>
                {rank}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Unit</InputLabel>
          <Select label="Unit" value={unitFilter} onChange={(e) => setUnitFilter(e.target.value)}>
            <MenuItem value="all">All</MenuItem>
            {uniqueUnits.map((unit_name) => (
              <MenuItem key={unit_name} value={unit_name}>
                {unit_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
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
                <TableCell>Unit</TableCell>
                <TableCell>Years of service</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.length > 0 ? (
                filtered.map((officer) => (
                  <TableRow key={officer.uid} hover>
                    <TableCell>
                      {officer.first_name} {officer.middle_name} {officer.last_name}
                    </TableCell>
                    <TableCell>{officer.employment?.latest_date ? "Inactive" : "Active"}</TableCell>
                    <TableCell>{officer.employment?.badge_number}</TableCell>
                    <TableCell>{officer.employment?.rank}</TableCell>
                    <TableCell>{officer.employment?.unit?.name}</TableCell>
                    <TableCell>
                      {officer.employment?.earliest_date} –{" "}
                      {officer.employment?.latest_date ?? "Current"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} sx={{ textAlign: "center", py: 4 }}>
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
