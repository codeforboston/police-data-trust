import ResultCardShell from "@/components/search/ResultCardShell"
import UnitResultContent from "@/components/search/result-content/UnitResultContent"
import { SearchResponse } from "@/utils/api"

type UnitListItemProps = {
  unit: SearchResponse
  isFirst?: boolean
  isLast?: boolean
  outlined?: boolean
}

export default function UnitListItem({
  unit,
  isFirst = false,
  isLast = false,
  outlined = false
}: UnitListItemProps) {
  return (
    <ResultCardShell
      href={`/unit/${unit.uid}`}
      isFirst={isFirst}
      isLast={isLast}
      outlined={outlined}
    >
      <UnitResultContent result={unit} />
    </ResultCardShell>
  )
}
