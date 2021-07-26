import { Feature } from "geojson"
import { useMemo, useState } from "react"
import uscities from "./uscities.json"

export interface GeoJson {
  type: string
  features: Feature[]
}

export interface Filter {
  property: string
  value: number | string
}

export interface Data {
  features: Feature[]
  filter: Filter
  setFilterProperties: (filter: Filter) => void
}

export default function useData(): Data {
  // using temp dummy data set
  const data: GeoJson = uscities as GeoJson

  const [filterProperties, setFilterProperties] = useState<Filter>({
    property: "state_name",
    value: "",
  })

  return useMemo(() => {
    const { property, value } = filterProperties

    const filteredFeatures =
      value === ""
        ? ([] as Feature[])
        : value === "all"
        ? data.features
        : data.features.filter((d: Feature) => d.properties[property] === value)

    return {
      features: filteredFeatures,
      filter: filterProperties,
      setFilterProperties,
    }
  }, [filterProperties])
}
