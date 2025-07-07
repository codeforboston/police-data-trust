"use client"
import { Tab, Tabs, Box, CardHeader, Typography } from "@mui/material"
import React, { useState } from "react"
import { SearchResult } from "./page"

type SearchResultsProps = {
  results: SearchResult[]
}

const SearchResults = ({ results }: SearchResultsProps) => {
  const [tab, setTab] = useState(0)

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setTab(newValue)
  }

  return (
    <>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={tab}
          onChange={handleChange}
          textColor="inherit"
          slotProps={{ indicator: { style: { backgroundColor: "black" } } }}
          sx={{
            "& .MuiTab-root": { color: "black" }
          }}>
          <Tab label="All" />
          <Tab label="Officer" />
          <Tab label="Complaint" />
          <Tab label="Agency" />
          <Tab label="Unit" />
          <Tab label="Litigation" />
        </Tabs>
      </Box>
      <Box sx={{ p: 3 }}>
        <Typography sx={{ marginBottom: "1rem", fontWeight: "bold" }}>
          {results.length} results
        </Typography>
        <CustomTabPanel value={tab} index={0}>
          {results.map((result) => (
            <CardHeader
              key={result.id}
              title={result.title}
              subheader={result.subtitle}
              slotProps={{ subheader: { fontWeight: "bold", color: "#000" } }}
              action={
                <Box sx={{ display: "flex", gap: "1rem" }}>
                  {result.tags.map((tag, index) => (
                    <span key={index} style={{ fontSize: "12px", color: "#666" }}>
                      {tag}
                    </span>
                  ))}
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
    </>
  )
}

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

const CustomTabPanel = ({ children, value, index, ...other }: TabPanelProps) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}>
      {value === index && <Box>{children}</Box>}
    </div>
  )
}
export default SearchResults
