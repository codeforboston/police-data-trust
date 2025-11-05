export type AccessToken = string

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

interface AuthenticatedRequest {
  accessToken: AccessToken
}

export interface SearchRequest extends AuthenticatedRequest {
  query: string
  location?: string
  source?: string
  page?: number
}

export type SearchResponse = {
  uid: string | number
  title: string
  subtitle: string
  content_type: string
  source: string
  last_updated: string
  description?: string
  tags?: string[]
}

export type PaginatedSearchResponses = {
  error?: string | null
  page?: number
  pages?: number
  per_page?: number
  total?: number
  results: SearchResponse[]
}
