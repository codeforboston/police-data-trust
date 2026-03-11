import { Box } from "@mui/material"
import { SearchResponse } from "@/utils/api"

type SearchResultMetaProps = {
  result: SearchResponse
}

export default function SearchResultMeta({ result }: SearchResultMetaProps) {
  return (
    <Box sx={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
      <Box component="span" sx={{ fontSize: "12px", color: "#566" }}>
        {result.content_type}
      </Box>
      <Box component="span" sx={{ fontSize: "12px", color: "#566" }}>
        {result.source}
      </Box>
      <Box component="span" sx={{ fontSize: "12px", color: "#566" }}>
        {result.last_updated}
      </Box>
    </Box>
  )
}