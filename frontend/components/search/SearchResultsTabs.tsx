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
          "& .MuiTab-root": { color: "black" },
          "& .MuiTab-root.Mui-disabled": {
            color: "#8b9198",
            opacity: 1,
            cursor: "not-allowed"
          }
        }}
      >
        <Tab label="All" />
        <Tab label="Officer" />
        <Tab label="Agency" />
        <Tab label="Unit" disabled />
        <Tab label="Complaint" disabled />
        <Tab label="Litigation" disabled />
      </Tabs>
    </Box>
  )
}
