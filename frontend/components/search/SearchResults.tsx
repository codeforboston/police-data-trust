"use client"

import { Box, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import SearchResultsTabs from "./SearchResultsTabs"
import SearchResultsList from "./SearchResultsList"
import { SearchTab } from "@/providers/SearchProvider"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
  tab: SearchTab
}

export default function SearchResults({ total, results, tab }: SearchResultsProps) {
  return (
    <>
      <SearchResultsTabs tab={tab} />

      <Box sx={{ p: 3 }}>
        <Typography sx={{ mb: 2, fontWeight: "bold" }}>{total} results</Typography>

        <SearchResultsList results={results} showMeta />
      </Box>
    </>
  )
}
