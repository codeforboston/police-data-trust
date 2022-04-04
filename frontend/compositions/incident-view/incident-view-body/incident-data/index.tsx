import { Incident } from "../../../../helpers/incident"
import styles from "./incident-data.module.css"

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
const { dataBlock, category, data, officerDisplay, officerColumn } = styles

export default function IncidentData(incident: Incident) {
  const { description } = incident
  // Need to make grid style, newline for departments
  return (
    <div>
      <div className={dataBlock}>
        <p className={category}>Summary:</p>
        <p className={data}>{description}</p>
      </div>
      <div className={dataBlock}>
        <p className={category}>Departments Involved:</p>
        <div>
          {incident.officers.map((officer) => (
            <p className={data} key={officer.badgeNo}>
              {officer.department}
            </p>
          ))}
        </div>
      </div>
      <div className={dataBlock}>
        <p className={category}>Officers Involved:</p>
        <div>{officerBox(incident.officers)}</div>
      </div>
    </div>
  )
}

function officerBox(officers: Incident["officers"]) {
  return (
    <div className={officerDisplay}>
      <div className={officerColumn}>
        <p className={category}>Officer Name</p>
        {officers.map((officer) => (
          <p className={data} key={officer.badgeNo}>
            {officer.firstName} {officer.lastName}
          </p>
        ))}
      </div>
      <div className={officerColumn}>
        <p className={category}>Badge No.</p>
        {officers.map((officer) => (
          <p className={data} key={officer.badgeNo}>
            {officer.badgeNo}
          </p>
        ))}
      </div>
    </div>
  )
}
