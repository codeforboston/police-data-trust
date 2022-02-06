import { OfficerRecordType } from "../../../models/officer"
import WorkHistoryInstance from "./work-history-instance"
import styles from "./officer-work-history.module.css"

export default function OfficerWorkHistory(officer: OfficerRecordType) {
  const { workHistory } = officer
  const { category, wrapper } = styles

  const result = workHistory.map((item, index) => (
    <WorkHistoryInstance key={index + "workHistoryItem"} {...item} />
  ))

  return (
    <div className={wrapper}>
      <div className={category}>
        <p>Work History Summary:</p>
      </div>
      <div>{result}</div>
    </div>
  )
}
