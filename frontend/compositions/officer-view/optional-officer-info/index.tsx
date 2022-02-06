import { OfficerRecordType } from "../../../models/officer"
import styles from "./optional-officer-info.module.css"

export default function OptionalOfficerInfo(officer: OfficerRecordType) {
  const { birthDate, gender, race, ethnicity, incomeBracket } = officer
  const { category, data, viewWrapper } = styles

  const dateString: string = new Date(birthDate).toLocaleDateString().split(",")[0]
  return (
    <div>
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
        <div className={data}>
          <p className={category}>Ethnicity</p>
          <p>{ethnicity}</p>
        </div>
        <div className={data}>
          <p className={category}>Income Bracket</p>
          <p>{incomeBracket}</p>
        </div>
      </div>
    </div>
  )
}
