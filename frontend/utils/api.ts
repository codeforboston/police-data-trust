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
  first_name?: string
  middle_name?: string
  last_name?: string
  suffix?: string | null
  ethnicity?: string
  gender?: string;
  state_ids?: any[] // TODO: create subtype
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
