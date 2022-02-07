import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-affiliations.module.css"

export default function OfficerAffiliations(officer: OfficerRecordType) {
  const { affiliations } = officer
  const { wrapper } = styles

  const affiliationsString = affiliations.join(", ")

  return (
    <div className={wrapper}>
      <p>Professional Affiliations: </p>
      <p>{affiliationsString}</p>
    </div>
  )
}
