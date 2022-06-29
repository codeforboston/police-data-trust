import { getOfficerFromMockData } from "./mock-to-officer-type"

/**
 * Modeled after incident.py in backend/database/models and design in FIGMA
 */

function sampleIncident() {
  return {
    id: 0,
    time_of_incident: "March 1, 2022",
    locationLonLat: [-71.0589, 42.3601] as [number, number],
    description:
      "Officer issued motorist ticket, use of excessive force resulted in civilian injury.",
    stop_type: "Traffic Stop",
    officers: [getOfficerFromMockData(0), getOfficerFromMockData(1)]
  }
}

export default function getIncident(id: number) {
  // TODO: Call the object from the db
  if (isNaN(id)) throw new Error("Not a number!")
  return sampleIncident()
}
