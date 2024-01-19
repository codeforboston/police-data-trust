import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-view-header.module.css"

export default function OfficerHeader(officer: OfficerRecordType) {
  const { firstName, lastName, knownEmployers } = officer
  const { name, title } = styles

  return (
    <div>
      <p className={title}>Officer Record</p>
      <p className={name}>
        {firstName} {lastName}
      </p>
    </div>
  )
}
