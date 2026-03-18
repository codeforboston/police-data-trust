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
  Paper
} from "@mui/material"
import { Search, TableRows, Apps } from "@mui/icons-material"
import { SearchResponse, Unit } from "@/utils/api"
import OfficerListItem from "@/components/officer/OfficerListItem"
import DetailCard from "@/components/Details/DetailCard"

type OfficerListProps = {
  unit: Unit
  officers?: SearchResponse[]
  activeOfficerCount?: number
  inactiveOfficerCount?: number
}

export default function OfficerList({
  unit,
  officers = [],
  activeOfficerCount,
  inactiveOfficerCount
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

  const filtered = officers.filter((officer) => {
    const name = officer.title?.toLowerCase() ?? ""
    const matchesSearch = searchValue.trim() === "" || name.includes(searchValue.toLowerCase())
    const matchesStatus = statusFilter === "all" || statusFilter === "active"
    const matchesRank = rankFilter === "all" || rankFilter === officer.subtitle
    const matchesUnit = unitFilter === "all" || unitFilter === unit.name

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
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="inactive">Inactive</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Rank</InputLabel>
          <Select label="Rank" value={rankFilter} onChange={(e) => setRankFilter(e.target.value)}>
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="Detective First Grade">Detective First Grade</MenuItem>
            <MenuItem value="Sergeant">Sergeant</MenuItem>
            <MenuItem value="Officer">Officer</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 160 }} size="small">
          <InputLabel>Unit</InputLabel>
          <Select label="Unit" value={unitFilter} onChange={(e) => setUnitFilter(e.target.value)}>
            <MenuItem value="all">All</MenuItem>
            <MenuItem value={unit.name ?? ""}>{unit.name}</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {viewMode === "table" ? (
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
                    <TableCell>{officer.title}</TableCell>
                    <TableCell>Active</TableCell>
                    <TableCell>{officer.uid}</TableCell>
                    <TableCell>{officer.subtitle}</TableCell>
                    <TableCell>{unit.name}</TableCell>
                    <TableCell>8 years</TableCell>
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
          {filtered.length > 0 ? (
            filtered.map((officer, index) => (
              <OfficerListItem
                key={officer.uid}
                officer={officer}
                outlined={false}
                isFirst={index === 0}
                isLast={index === filtered.length - 1}
              />
            ))
          ) : (
            <Typography sx={{ py: 4, textAlign: "center" }}>No officers found.</Typography>
          )}
        </DetailCard>
      )}
    </Box>
  )
}
