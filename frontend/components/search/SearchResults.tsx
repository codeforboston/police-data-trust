"use client"

import { Box, Typography } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import SearchResultsTabs from "./SearchResultsTabs"
import SearchResultsList from "./SearchResultsList"
import NoExactMatchNotice from "./NoExactMatchNotice"
import { SearchTab } from "@/providers/SearchProvider"
import { hasNoExactMatch, noResultsMessage } from "@/utils/noResults"

type SearchResultsProps = {
  total: number
  results: SearchResponse[]
  tab: SearchTab
  term?: string
  hasFilters?: boolean
  page?: number
  // A search ran and its answer is shown (not the empty page before any search).
  searched?: boolean
}

export default function SearchResults({
  total,
  results,
  tab,
  term = "",
  hasFilters = false,
  page = 1,
  searched = false
}: SearchResultsProps) {
  const message = noResultsMessage(term, hasFilters)
  const noResults = searched && results.length === 0
  // Partial matches only: say so above them, on the first page.
  const noExactMatch = page === 1 && hasNoExactMatch(results)

  return (
    <>
      <SearchResultsTabs tab={tab} />

      <Box sx={{ p: 3 }}>
        {noResults ? (
          <Typography role="status" sx={{ textAlign: "center", py: 2 }}>
            {message}
          </Typography>
        ) : (
          <>
            {noExactMatch && <NoExactMatchNotice message={message} />}

            <Typography sx={{ mb: 2, fontWeight: "bold" }}>{total} results</Typography>

            <SearchResultsList results={results} showMeta />
          </>
        )}
      </Box>
    </>
  )
}
