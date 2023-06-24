import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-view-header.module.css"

export default function OfficerHeader(officer: OfficerRecordType) {
  const { firstName, lastName, knownEmployers } = officer
  const { category, name, titleAndName, otherData, viewWrapper } = styles

  return (
    <div>
      <h3>Officer Record</h3>
      <div className={viewWrapper}>
        <div className={titleAndName}>
          <p className={name}>
            {firstName} {lastName}
          </p>
        </div>
        <div className={otherData}>
          <p className={category}>Known Employers</p>
          <p>{knownEmployers[0]}</p>
        </div>
      </div>
    </div>
  )
}
