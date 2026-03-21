import { Box } from "@mui/material"
import { SearchResponse } from "@/utils/api"
import ResultCardShell from "./ResultCardShell"
import SearchResultMeta from "./SearchResultMeta"
import SearchResultContent from "./result-content/SearchResultContent"
import getResultHref from "./getResultHref"

type SearchResultCardProps = {
  result: SearchResponse
  isFirst?: boolean
  isLast?: boolean
  showMeta?: boolean
}

export default function SearchResultCard({
  result,
  isFirst = false,
  isLast = false,
  showMeta = true
}: SearchResultCardProps) {
  return (
    <ResultCardShell href={getResultHref(result)} isFirst={isFirst} isLast={isLast}>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
        <SearchResultContent result={result} />
        {showMeta && <SearchResultMeta result={result} />}
      </Box>
    </ResultCardShell>
  )
}
