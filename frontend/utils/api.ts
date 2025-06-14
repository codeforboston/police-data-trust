// import axiosModule, { AxiosRequestConfig } from "axios"

export type AccessToken = string

// export interface User {
//   active: boolean
//   role: string
//   email: string
//   emailConfirmedAt?: string
//   firstname?: string
//   lastname?: string
//   phone_number?: string
// }

// export interface NewUser {
//   email: string
//   password: string
//   firstname?: string
//   lastname?: string
//   phone_number?: string
// }

// export interface LoginCredentials {
//   email: string
//   password: string
// }

// export interface ForgotPassword {
//   email: string
// }

// export interface ResetPasswordRequest extends AuthenticatedRequest {
//   accessToken: string
//   password: string
// }

// export interface ResetPasswordResponse {
//   message: string
// }

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

// export enum Rank {
//   TECHNICIAN = "Technician",
//   OFFICER = "Officer",
//   DETECTIVE = "Detective",
//   CORPORAL = "Corporal",
//   SERGEANT = "Sergeant",
//   LIEUTENANT = "Lieutenant",
//   CAPTAIN = "Captain",
//   DEPUTY = "Deputy",
//   CHIEF = "Chief",
//   COMMISSIONER = "Commissioner"
// }

// export interface Officer {
//   id?: number
//   first_name?: string
//   last_name?: string
//   race?: string
//   ethnicity?: string
//   gender?: string
//   rank?: Rank
//   star?: string
//   date_of_birth?: Date
// }

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

// export type RegisterRequest = NewUser
// export type LoginRequest = LoginCredentials
// export type WhoamiRequest = AuthenticatedRequest
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

export async function searchIncidents({
  accessToken,
  dateStart,
  dateEnd,
  ...rest
}: IncidentSearchRequest): Promise<IncidentSearchResponse> {
  if (dateStart) dateStart = new Date(dateStart).toISOString().slice(0, -1)
  if (dateEnd) dateEnd = new Date(dateEnd).toISOString().slice(0, -1)

  return fetch("/incidents/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({ dateStart, dateEnd, ...rest })
    })
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch incidents");
      return res.json();
    });
}
