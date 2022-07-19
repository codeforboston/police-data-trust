import type { Incident } from "../helpers/api"
import type { OfficerRecordType } from "./officer"

export interface IncidentRecordType extends Omit<Incident, "officers"> {
  stop_type?: string
  officers: OfficerRecordType[]
}
