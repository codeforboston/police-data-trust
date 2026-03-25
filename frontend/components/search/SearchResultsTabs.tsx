"use client"

import React from "react"
import { Box, Tab, Tabs } from "@mui/material"

type SearchResultsTabsProps = {
  tab: number
  updateTab: (val: number) => void
}

export default function SearchResultsTabs({ tab, updateTab }: SearchResultsTabsProps) {
  return (
    <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
      <Tabs
        value={tab}
        onChange={(_e: React.SyntheticEvent, newValue: number) => updateTab(newValue)}
        textColor="inherit"
        slotProps={{ indicator: { style: { backgroundColor: "black" } } }}
        sx={{
          "& .MuiTab-root": { color: "black" }
        }}
      >
        <Tab label="All" />
        <Tab label="Officer" />
        <Tab label="Complaint" />
        <Tab label="Agency" />
        <Tab label="Unit" />
        <Tab label="Litigation" />
      </Tabs>
    </Box>
  )
}
