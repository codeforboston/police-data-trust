"use client"

import { Box, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import SearchResultsTabs from "./SearchResultsTabs"
import SearchResultsList from "./SearchResultsList"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
  tab: number
  updateTab: (val: number) => void
}

export default function SearchResults({ total, results, tab, updateTab }: SearchResultsProps) {
  return (
    <>
      <SearchResultsTabs tab={tab} updateTab={updateTab} />

      <Box sx={{ p: 3 }}>
        <Typography sx={{ mb: 2, fontWeight: "bold" }}>{total} results</Typography>

        <SearchResultsList results={results} showMeta />
      </Box>
    </>
  )
}
