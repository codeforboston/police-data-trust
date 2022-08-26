import IncidentData from "./incident-data"
import Map from "./incident-google-map"
import type { Incident } from "../../../helpers/api"
import styles from "./incident-body.module.css"

export default function IncidentBody(incident: Incident) {
  const { bodyWrapper } = styles
  return (
    <div className={bodyWrapper}>
      <Map {...incident} />
      <IncidentData {...incident} />
    </div>
  )
}
