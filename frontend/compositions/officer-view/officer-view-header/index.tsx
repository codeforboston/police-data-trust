import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-view-header.module.css"

export default function OfficerHeader(officer: OfficerRecordType) {
  const { firstName, lastName, badgeNo, status, department } = officer
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
          <p className={category}>Badge Number</p>
          <p>{badgeNo}</p>
        </div>
        <div className={otherData}>
          <p className={category}>Officer Status</p>
          <p>{status}</p>
        </div>
        <div className={otherData}>
          <p className={category}>Department</p>
          <p>{department}</p>
        </div>
      </div>
    </div>
  )
}
