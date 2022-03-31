import { Incident } from "../../../helpers/sample-incident"
import styles from "./incident-view-header.module.css"

/*
export interface Incident {
  id: number
  time_of_incident: Date
  location: { latitude: number; longitude: number }
  description: string // A summary of what happened
  stop_type: string // Reason for stop. ie Traffic Stop
  officers: OfficerRecordType[]
}
*/
export default function IncidentViewHeader(incident: Incident) {
  const { id, stop_type, time_of_incident } = incident
  const { wrapper, idAndStop, data, category } = styles

  const date = time_of_incident.toDateString()
  const time = time_of_incident.toTimeString()

  return (
    <div className={wrapper}>
      <div className={idAndStop}>
        <strong>{id}</strong>
        <p>{stop_type}</p>
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
