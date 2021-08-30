import { Feature } from "geojson"

export interface GeoJson {
  type: string
  features: Feature[]
}

export interface Filter {
  property: string
  value: number | string
  sliceMin?: number
  sliceMax?: number
}

export interface Data {
  features: Feature[]
  filter: Filter
  setFilterProperties: (filter: Filter) => void
}

export interface CityProperties {
  city: string
  city_ascii: string
  state_id: string
  state_name: string
  county_fips: number
  county_name: string
  population: number
  density: number
  source: string
  military: boolean | string
  incorporated: boolean | string
  timezone: string
  ranking: number
  zips: number[] | string
  id: number
}
