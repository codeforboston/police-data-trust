import { OfficerRecordType } from "../models/officer"
import { getOfficerFromMockData } from "./mock-to-officer-type"

/**
 * Modeled after incident.py in backend/database/models and design in FIGMA
 */
export interface Incident {
  id: number
  time_of_incident: Date
  location: { latitude: number; longitude: number }
  description: string // A summary of what happened
  stop_type: string // Reason for stop. ie Traffic Stop
  officers: OfficerRecordType[]
}

export default function sampleIncident(): Incident {
  return {
    id: 0,
    time_of_incident: new Date('March 1, 2022 00:00:00'),
    location: { latitude: 0, longitude: 0 },
    description:
      "Officer issued motorist ticket, use of excessive force resulted in civilian injury.",
    stop_type: "Traffic Stop",
    officers: [getOfficerFromMockData(0), getOfficerFromMockData(1)]
  }
}
