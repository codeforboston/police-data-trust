import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-affiliations.module.css"

export default function OfficerAffiliations(officer: OfficerRecordType) {
  const { affiliations } = officer

  let affiliationsString = ""
  for (const union of affiliations) {
    affiliationsString += union + ", "
  }

  return (
    <div style={{ display: "flex" }}>
      <p>Professional Affiliations: </p>
      <p>{affiliationsString}</p>
    </div>
  )
}
