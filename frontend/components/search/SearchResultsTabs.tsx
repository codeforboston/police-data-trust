"use client"

import React from "react"
import { Box, Tab, Tabs } from "@mui/material"
import { SearchTab, useSearch } from "@/providers/SearchProvider"

type SearchResultsTabsProps = {
  tab: SearchTab
}

export default function SearchResultsTabs({ tab }: SearchResultsTabsProps) {
  const { setTab } = useSearch()

  return (
    <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
      <Tabs
        value={tab}
        onChange={(_e: React.SyntheticEvent, newValue: SearchTab) => setTab(newValue)}
        textColor="inherit"
        slotProps={{ indicator: { style: { backgroundColor: "black" } } }}
        sx={{
          "& .MuiTab-root": { color: "black" },
          "& .MuiTab-root.Mui-disabled": {
            color: "#8b9198",
            opacity: 1,
            cursor: "not-allowed"
          }
        }}
      >
        <Tab value="all" label="All" />
        <Tab value="officers" label="Officer" />
        <Tab value="agencies" label="Agency" />
        <Tab value="units" label="Unit" disabled />
        <Tab value="complaints" label="Complaint" disabled />
        <Tab value="litigation" label="Litigation" disabled />
      </Tabs>
    </Box>
  )
}
