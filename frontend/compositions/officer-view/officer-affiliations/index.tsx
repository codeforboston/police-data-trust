import { OfficerRecordType } from "../../../models/officer"
import styles from "./officer-affiliations.module.css"

export default function OfficerAffiliations(officer: OfficerRecordType) {
  const { affiliations } = officer
  const { wrapper } = styles


  return (
    <div className={wrapper}>
      <p>Professional Affiliations: </p>
    </div>
  )
}
