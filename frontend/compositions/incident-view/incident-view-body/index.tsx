import IncidentData from "./incident-data"
import Map from "./incident-google-map"
import { IncidentRecordType } from "../../../models"
import styles from "./incident-body.module.css"

export default function IncidentBody(incident: IncidentRecordType) {
  const { bodyWrapper } = styles
  return (
    <div className={bodyWrapper}>
      <Map {...incident} />
      <IncidentData {...incident} />
    </div>
  )
}
