import { Incident } from "../../../helpers/incident"
import styles from "./incident-view-header.module.css"

export default function IncidentViewHeader(incident: Incident) {
  const { id, stop_type, time_of_incident } = incident
  const { wrapper, idAndStop, data, category, stopType } = styles

  const date = time_of_incident.toDateString()
  const time = time_of_incident.toTimeString()

  return (
    <div className={wrapper}>
      <div className={idAndStop}>
        <strong>{id}</strong>
        <p className={stopType}>{stop_type}</p>
      </div>
      <div className={data}>
        <p className={category}>Date</p>
        <p>{date}</p>
      </div>
      <div className={data}>
        <p className={category}>Time</p>
        <p>{time}</p>
      </div>
      <div className={data}>
        <p className={category}>Location</p>
        <p>TODO: Possibly use Google Maps API</p>
      </div>
    </div>
  )
}
