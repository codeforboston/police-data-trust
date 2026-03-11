import ResultCardShell from "@/components/search/ResultCardShell"
import OfficerResultContent from "@/components/search/result-content/OfficerResultContent"
import { SearchResponse } from "@/utils/api"

type OfficerListItemProps = {
  officer: SearchResponse
  isFirst?: boolean
  isLast?: boolean
  outlined?: boolean
}

export default function OfficerListItem({
  officer,
  isFirst = false,
  isLast = false,
  outlined = false
}: OfficerListItemProps) {
  return (
    <ResultCardShell
      href={`/officer/${officer.uid}`}
      isFirst={isFirst}
      isLast={isLast}
      outlined={outlined}
    >
      <OfficerResultContent result={officer} />
    </ResultCardShell>
  )
}