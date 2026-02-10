"use client"
import { Tab, Tabs, Box, CardHeader, Typography } from "@mui/material"
import React from "react"
import { SearchResponse } from "@/utils/api"
import { useRouter } from "next/navigation"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
  tab: number
  updateTab: (val: number) => void
}

const SearchResults = ({ total, results, tab, updateTab }: SearchResultsProps) => {
  const router = useRouter()

  const handleResultClick = (result: SearchResponse) => {
    // Navigate to officer page if content type is Officer
    if (result.content_type.toLowerCase() === "officer") {
      router.push(`/officer?uid=${result.uid}`)
    }
  }

  const isClickable = (result: SearchResponse) => {
    return result.content_type.toLowerCase() === "officer"
  }

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
        <Typography sx={{ marginBottom: "1rem", fontWeight: "bold" }}>{total} results</Typography>
        <CustomTabPanel value={tab} index={tab}>
          {results.map((result) => (
            <CardHeader
              key={result.uid}
              title={result.title}
              subheader={result.subtitle}
              slotProps={{ subheader: { fontWeight: "bold", color: "#000" } }}
              action={
                <Box>
                  <Box sx={{ display: "flex", gap: "1rem" }}>
                    <span style={{ fontSize: "14px", color: "#454C54", margin: "0 0 1rem 0" }}>
                      {result.details}
                    </span>
                  </Box>
                  <Box sx={{ display: "flex", gap: "1rem" }}>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.content_type}</span>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.source}</span>
                    <span style={{ fontSize: "12px", color: "#666" }}>{result.last_updated}</span>
                  </Box>
                </Box>
              }
              onClick={() => handleResultClick(result)}
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
                paddingBlock: "2rem",
                cursor: isClickable(result) ? "pointer" : "default",
                transition: "background-color 0.2s",
                "&:hover": isClickable(result)
                  ? {
                      backgroundColor: "#f5f5f5"
                    }
                  : {}
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
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  )
}
export default SearchResults
