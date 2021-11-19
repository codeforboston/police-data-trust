import { Incident } from "../helpers/api"

// SAVED RESULTS DATA TABLE
export interface SavedResultsType extends Incident {
  searchDate: number // UNIX timestamp
}

// SAVED SEARCHES DATA TABLE
export interface SavedSearchType {
  searchDate: number // UNIX timestamp
  who: string[]
  what: string
  when: number // UNIX timestamp
  where: string
  total: number
  results: number
}
