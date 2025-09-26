"use client"
import { Tab, Tabs, Box, CardHeader, Typography } from "@mui/material"
import React, { useState } from "react"
import { SearchResponse } from "@/utils/api"
import { useSearch } from "@/providers/SearchProvider"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
}

const SearchResults = ({ total, results }: SearchResultsProps) => {
  const { loading, view, updateView } = useSearch()

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    updateView(newValue)
  }

  return (
    <>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={view}
          onChange={handleChange}
          textColor="inherit"
          slotProps={{ indicator: { style: { backgroundColor: "black" } } }}
          sx={{
            "& .MuiTab-root": { color: "black" }
          }}
        >
          <Tab label="All" value={'all'} />
          <Tab label="Officer" value={'officers'} />
          <Tab label="Complaint" value={'complaints'}/>
          <Tab label="Agency" value={'agencies'}/>
          <Tab label="Unit" value={'units'} />
          <Tab label="Litigation" value={'litigations'} />
        </Tabs>
      </Box>
      {loading ? (
        <Box sx={{ p: 3, textAlign: "center" }}>
          <Typography>Loading...</Typography>
        </Box>
      ) : (
        <Box sx={{ p: 3 }}>
          <Typography sx={{ marginBottom: "1rem", fontWeight: "bold" }}>{total} results</Typography>
          <CustomTabPanel value={view} index={'all'}>
            {results.map((result) => (
              <CardHeader
                key={result.uid}
                title={result.title}
                subheader={result.subtitle}
                slotProps={{ subheader: { fontWeight: "bold", color: "#000" } }}
                action={
                  <Box sx={{ display: "flex", gap: "1rem" }}>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.content_type}</span>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.source}</span>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.last_updated}</span>
                  </Box>
                }
                sx={{
                  flexDirection: "column",
                  alignItems: "flex-start",
                  gap: "0.5rem",
                  border: "1px solid #ddd",
                  borderBottom: "none",
                  ":first-of-type": {
                    borderTopLeftRadius: "4px",
                    borderTopRightRadius: "4px"
                  },
                  ":last-of-type": {
                    borderBottomLeftRadius: "4px",
                    borderBottomRightRadius: "4px",
                    borderBottom: "1px solid #ddd"
                  },
                  "& .MuiCardHeader-content": {
                    overflow: "hidden"
                  },
                  paddingInline: "4.5rem",
                  paddingBlock: "2rem"
                }}
              />
            ))}
          </CustomTabPanel>
        </Box>
      )}
    </>
  )
}

interface TabPanelProps {
  children?: React.ReactNode
  index: string
  value: string
}

const CustomTabPanel = ({ children, value, index, ...other }: TabPanelProps) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  )
}
export default SearchResults
