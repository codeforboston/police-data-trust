import { OfficerRecordType } from "../../../models/officer"
import styles from "./optional-officer-info.module.css"

export default function OptionalOfficerInfo(officer: OfficerRecordType) {
  const { dateOfBirth, gender, race, ethnicity, badgeNo, status, department } = officer
  const { category, data, viewWrapper } = styles

  const dateString: string = new Date(dateOfBirth).toLocaleDateString().split(",")[0]
  return (
    <>
      <div className={viewWrapper}>
        <div className={data}>
          <p className={category}>Badge Number</p>
          <p>{badgeNo}</p>
        </div>
        <div className={data}>
          <p className={category}>Officer Status</p>
          <p>{status}</p>
        </div>
        <div className={data}>
          <p className={category}>Department</p>
          <p>{department}</p>
        </div>
      </div>
      <div className={viewWrapper}>
        <div className={data}>
          <p className={category}>Date of Birth</p>
          <p>{dateString}</p>
        </div>
        <div className={data}>
          <p className={category}>Gender</p>
          <p>{gender}</p>
        </div>
        <div className={data}>
          <p className={category}>Race</p>
          <p>{race}</p>
        </div>
      </div>
      <div>
        <div className={viewWrapper}>
          <div className={data}>
            <p className={category}>Ethnicity</p>
            <p>{ethnicity}</p>
          </div>
        </div>
      </div>
    </>
  )
}
