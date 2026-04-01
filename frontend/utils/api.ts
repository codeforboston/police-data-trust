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

export type SearchContentType = "Officer" | "Agency" | "Unit" | "Complaint" | "Litigation"

export type SearchResponse = {
  uid: string | number
  title: string
  subtitle: string
  content_type: SearchContentType
  source: string
  last_updated: string
  description?: string
  tags?: string[]
  first_name?: string
  middle_name?: string
  last_name?: string
  suffix?: string | null
  ethnicity?: string
  gender?: string
  state_ids?: any[] // TODO: replace with subtype
  details?: string[]
}

export type PaginatedSearchResponses = {
  error?: string | null
  page?: number
  pages?: number
  per_page?: number
  total?: number
  results: SearchResponse[]
}

export interface SocialMedia {
  twitter_url?: string
  facebook_url?: string
  linkedin_url?: string
  instagram_url?: string
  youtube_url?: string
  tiktok_url?: string
}

export interface ContactInfo {
  additional_emails: string[]
  phone_numbers: string[]
}

export interface UserProfile {
  uid: string
  first_name: string
  last_name: string
  primary_email: string
  contact_info: ContactInfo
  location?: {
    city?: string
    state?: string
  }
  employment?: {
    employer?: string
    title?: string
  }
  bio?: string
  profile_image?: string
  social_media?: SocialMedia
  website?: string
  role: string
  active: boolean
}

export type UpdateUserProfilePayload = {
  first_name?: string
  last_name?: string
  bio?: string
  title?: string
  organization?: string
  location?: {
    city?: string
    state?: string
  }
  employment?: {
    employer?: string
    title?: string
  }
  contact_info?: {
    additional_emails?: string[]
    phone_numbers?: string[]
  }
  website?: string
  social_media?: {
    twitter_url?: string
    facebook_url?: string
    linkedin_url?: string
    instagram_url?: string
    youtube_url?: string
    tiktok_url?: string
  }
  primary_email?: string
}

export type Organization = {
  uid?: string
  name: string
  description: string
  logo: string
  website: string
  email: string
  location?: {
    city?: string
    state?: string
  }
  type_of_service: string
}

export type StateID = {
  uid: string
  state: string
  id_name: string
  value: string
}

export type EmploymentHistory = {
  earliest_date?: string
  badge_number?: string
  highest_rank?: string
  latest_date?: string
  salary?: number
  unit_name?: string
  agency_name?: string
  state?: string
  agency_uid?: string
  unit_uid?: string
}

export type AllegationSummary = {
  type: string
  complaint_count: number
  count: number
  substantiated_count: number
  earliest_incident_date?: string
  latest_incident_date?: string
}

export type UnitMostComplaints = {
  unit_name: string
  officer_count: number
  complaint_count: number
  unit_uid: string
}

export type OfficerMostComplaints = {
  officer_uid: string
  first_name: string
  last_name: string
  suffix?: string | null
  gender: string
  ethnicity: string
  rank: string
  complaint_count: number
  allegation_count: number
}

export type Location = {
  latitude: number
  longitude: number
  city?: string
  state?: string
}

export type OfficerEmployment = {
  uid: string
  earliest_date?: string
  latest_date?: string
  badge_number?: string
  rank?: string
  unit?: {
    uid: string
    name: string
  }
}

export type Officer = {
  uid: string
  first_name: string
  middle_name?: string
  last_name: string
  suffix?: string
  ethnicity?: string
  gender?: string
  year_of_birth?: string
  state_ids?: StateID[]
  employment?: OfficerEmployment
  employment_history?: EmploymentHistory[]
  allegation_summary?: AllegationSummary[]
  sources?: Source[]
}

export type Agency = {
  uid: string
  name: string
  location?: Location
  hq_state: string
  hq_city?: string
  hq_address?: string
  hq_zip?: string
  description?: string
  website_url?: string
  phone?: string
  jurisdiction?: string
  total_units?: number
  total_officers?: number
  total_complaints?: number
  allegation_summary?: AllegationSummary[]
  most_reported_units?: SearchResponse[]
  sources?: Source[]
}

export type Unit = {
  uid: string
  name: string
  location?: Location
  most_reported_officers?: SearchResponse[]
  total_officers?: number
  total_complaints?: number
  total_allegations?: number
  agency?: Agency
  sources?: Source[]
}
