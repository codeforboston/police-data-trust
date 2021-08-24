import { IconDefinition } from "@fortawesome/free-solid-svg-icons"

export interface IncidentData {
  dates: string
  incidentType: string
  officersInvolved: string[]
  subject: IconDefinition
  source: IconDefinition
}

// TODO: Add a unique id that will be needed as a key prop as soon
// as the precise shape and types of back-end data are known.
