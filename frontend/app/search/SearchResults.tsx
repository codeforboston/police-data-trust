"use client"

import Link from "next/link"
import { Tab, Tabs, Box, Card, CardHeader, CardActionArea, Typography } from "@mui/material"
import React from "react"
import { SearchResponse } from "@/utils/api"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
  tab: number
  updateTab: (val: number) => void
}

const getResultHref = (result: SearchResponse) => {
  switch (result.content_type) {
    case "Officer":
      return `/officer/${result.uid}`
    case "Agency":
      return `/agency/${result.uid}`
    case "Unit":
      return `/unit/${result.uid}`
    case "Complaint":
      return `/complaint/${result.uid}`
    case "Litigation":
      return `/litigation/${result.uid}`
    default:
      return "#"
  }
}

const SearchResults = ({ total, results, tab, updateTab }: SearchResultsProps) => {
  return (
    <>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={tab}
          onChange={(e: React.SyntheticEvent, newValue: number) => updateTab(newValue)}
          textColor="inherit"
          slotProps={{ indicator: { style: { backgroundColor: "black" } } }}
          sx={{
            "& .MuiTab-root": { color: "black" }
          }}
        >
          <Tab key="all" label="All" />
          <Tab key="officer" label="Officer" />
          <Tab key="complaint" label="Complaint" />
          <Tab key="agency" label="Agency" />
          <Tab key="unit" label="Unit" />
          <Tab key="litigation" label="Litigation" />
        </Tabs>
      </Box>

      <Box sx={{ p: 3 }}>
        <Typography sx={{ mb: 2, fontWeight: "bold" }}>{total} results</Typography>

        <CustomTabPanel value={tab} index={tab}>
          {results.map((result, idx) => (
            <Card
              key={result.uid}
              variant="outlined"
              sx={{
                borderBottomLeftRadius: idx === results.length - 1 ? "4px" : 0,
                borderBottomRightRadius: idx === results.length - 1 ? "4px" : 0,
                borderTopLeftRadius: idx === 0 ? "4px" : 0,
                borderTopRightRadius: idx === 0 ? "4px" : 0,
                borderBottom: idx === results.length - 1 ? undefined : "none"
              }}
            >
              <CardActionArea
                component={Link}
                href={getResultHref(result)}
                sx={{
                  display: "block",
                  textAlign: "left",
                  "&:hover": {
                    backgroundColor: "#f8f8f8"
                  }
                }}
              >
                <CardHeader
                  title={result.title}
                  subheader={result.subtitle}
                  slotProps={{ subheader: { fontWeight: "bold", color: "#000" } }}
                  action={
                    <Box>
                      <Box sx={{ display: "flex", gap: "1rem" }}>
                        <span
                          style={{
                            fontSize: "14px",
                            color: "#454C54",
                            margin: "0 0 1rem 0"
                          }}
                        >
                          {Array.isArray(result.details)
                            ? result.details.join(", ")
                            : result.details}
                        </span>
                      </Box>

                      <Box sx={{ display: "flex", gap: "1rem" }}>
                        <span style={{ fontSize: "12px", color: "#566" }}>
                          {result.content_type}``
                        </span>
                        <span style={{ fontSize: "12px", color: "#566" }}>{result.source}</span>
                        <span style={{ fontSize: "12px", color: "#566" }}>
                          {result.last_updated}
                        </span>
                      </Box>
                    </Box>
                  }
                  sx={{
                    flexDirection: "column",
                    alignItems: "flex-start",
                    gap: "0.5rem",
                    "& .MuiCardHeader-content": {
                      overflow: "hidden"
                    },
                    paddingInline: "4.5rem",
                    paddingBlock: "2rem"
                  }}
                />
              </CardActionArea>
            </Card>
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
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  )
}

export default SearchResults
