import { SearchResponse } from "@/utils/api"
import SearchResultCard from "./SearchResultCard"

type SearchResultsListProps = {
  results: SearchResponse[]
  showMeta?: boolean
}

export default function SearchResultsList({
  results,
  showMeta = true
}: SearchResultsListProps) {
  return (
    <>
      {results.map((result, idx) => (
        <SearchResultCard
          key={result.uid}
          result={result}
          isFirst={idx === 0}
          isLast={idx === results.length - 1}
          showMeta={showMeta}
        />
      ))}
    </>
  )
}
