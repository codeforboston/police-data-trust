import { OfficerRecordType } from "../../../models/officer"
import WorkHistoryInstance from "./work-history-instance"
import styles from "./officer-work-history.module.css"

export default function OfficerWorkHistory(officer: OfficerRecordType) {
  const { workHistory } = officer
  const { category, workInstanceBlock } = styles

  let result: JSX.Element[] = []
  for (const workInstance of workHistory) {
    result.push(<WorkHistoryInstance {...workInstance} />)
  }

  return (
    <div style={{ display: "flex" }}>
      <div className={category}>
        <p>Work History Summary:</p>
      </div>
      <div>{result}</div>
    </div>
  )
}
