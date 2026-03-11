import { SearchResponse } from "@/utils/api"
import OfficerResultContent from "./OfficerResultContent"
import GenericResultContent from "./GenericResultContent"

type SearchResultContentProps = {
  result: SearchResponse
}

export default function SearchResultContent({ result }: SearchResultContentProps) {
  switch (result.content_type) {
    case "Officer":
      return <OfficerResultContent result={result} />
    default:
      return <GenericResultContent result={result} />
  }
}
