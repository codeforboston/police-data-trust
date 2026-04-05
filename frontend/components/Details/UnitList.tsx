"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
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
import { Unit, Agency } from "@/utils/api"
import DetailCard from "@/components/Details/DetailCard"

type UnitListProps = {
  agency: Agency
  units?: Unit[]
  activeUnitCount?: number
  inactiveUnitCount?: number
  loading?: boolean
  error?: Error | null
}

export default function UnitList({
  agency,
  units = [],
  activeUnitCount,
  inactiveUnitCount,
  loading = false,
  error = null
}: UnitListProps) {
  const router = useRouter()
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

  const activeCount = activeUnitCount ?? agency.total_units ?? 0
  const inactiveCount = inactiveUnitCount ?? 0

  // Extract unique values for filter dropdowns
  const uniqueStatuses = React.useMemo(() => {
    const statuses = new Set<string>()
    units.forEach((unit) => {
      const status = "Active"
      statuses.add(status)
    })
    return Array.from(statuses).sort()
  }, [units])

  const filtered = units.filter((unit) => {
    const name =
      `${unit.name}`.toLowerCase() || ""
    const matchesSearch = searchValue.trim() === "" || name.includes(searchValue.toLowerCase())

    const status = "Active"
    const matchesStatus = statusFilter === "all" || statusFilter === status



    return matchesSearch && matchesStatus
  })

  return (
    <Box>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2, alignItems: "center" }}>
        <Box sx={{ flexGrow: 1, minWidth: 240 }}>
          <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: 500 }}>
            Units list
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary", mt: 0.5 }}>
            {activeCount} active units · {inactiveCount} deactivated units
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
          placeholder="search unit or try anything"
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
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <MenuItem value="all">All</MenuItem>
            {uniqueStatuses.map((status) => (
              <MenuItem key={status} value={status}>
                {status}
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
          Could not load units.
        </Typography>
      ) : viewMode === "table" ? (
        <Paper sx={{ width: "100%", mt: 3, overflowX: "auto" }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Unit name</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.length > 0 ? (
                filtered.map((unit) => (
                  <TableRow
                    key={unit.uid}
                    hover
                    onClick={() => router.push(`/unit/${unit.uid}`)}
                    sx={{
                      cursor: "pointer",
                      "&:hover": { backgroundColor: "action.hover" }
                    }}
                  >
                    <TableCell>
                      {unit.name}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={1} sx={{ textAlign: "center", py: 4 }}>
                    No units found.
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
