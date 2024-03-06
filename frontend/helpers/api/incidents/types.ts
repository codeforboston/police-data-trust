import { AuthenticatedRequest } from "../base"

export interface Source {
  name?: string
  id?: number
  url?: string
  contact_email?: string
}

export interface Perpetrator {
  first_name?: string
  last_name?: string
}

export enum Rank {
  TECHNICIAN = "Technician",
  OFFICER = "Officer",
  DETECTIVE = "Detective",
  CORPORAL = "Corporal",
  SERGEANT = "Sergeant",
  LIEUTENANT = "Lieutenant",
  CAPTAIN = "Captain",
  DEPUTY = "Deputy",
  CHIEF = "Chief"
}

export interface Officer {
  id?: number
  first_name?: string
  last_name?: string
  race?: string
  ethnicity?: string
  gender?: string
  rank?: Rank
  star?: string
  date_of_birth?: Date
}

export interface UseOfForce {
  item?: string
}

export interface Incident {
  id: number
  source?: Source
  source_id?: number
  location?: string
  locationLonLat?: [number, number] //TODO: Backend data does not return locationLonLat attribute. Remove this and refactor frontend
  latitude?: number
  longitude?: number
  time_of_incident?: string
  department?: string
  perpetrators: Perpetrator[]
  description?: string
  use_of_force?: UseOfForce[]
}

export interface IncidentSearchRequest extends AuthenticatedRequest {
  description?: string
  dateStart?: string
  dateEnd?: string
  location?: string
  source?: string
  page?: number
  perPage?: number
}

export type IncidentSearchResponse = {
  results: Incident[]
  page: number
  totalPages: number
  totalResults: number
}
