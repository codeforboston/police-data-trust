import { OfficerRecordType } from "../../../models/officer"
import WorkHistoryInstance from "./work-history-instance"
import styles from "./officer-work-history.module.css"

export default function OfficerWorkHistory(officer: OfficerRecordType) {
  const { workHistory } = officer
  const { wrapper, title } = styles

  const result = workHistory.map((item, index) => (
    <WorkHistoryInstance key={index + "workHistoryItem"} {...item} />
  ))

  return (
    <div className={wrapper}>
      <p className={title}>Work History:</p>
      <div>{result}</div>
    </div>
  )
}
