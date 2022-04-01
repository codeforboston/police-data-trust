import { Incident } from "../../../../helpers/incident"
import styles from './incident-data.module.css'

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

export default function IncidentData(incident: Incident) {
    const { dataBlock, category, data } = styles
    const { description } = incident

    function officerDepartments(officers: Incident["officers"]) {
        return officers.map((officer) => {
            return <p key={officer.badgeNo}>{officer.department}</p>
        })
    }

    // Need to make grid style, newline for departments
    return (
        <div>
            <div className={dataBlock}>
                <p className={category}>Summary:</p>
                <p className={data}>{description}</p>
            </div>
            <div className={dataBlock}>
                <p className={category}>Departments Involved:</p> 
                {officerDepartments(incident.officers)}
            </div>
        </div>
    )
}