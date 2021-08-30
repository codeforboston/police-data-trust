import { Feature } from "geojson"
import { useMemo, useState } from "react"
import uscities from "./uscities.json"
import { GeoJson, Filter, Data } from "../../../models"

export default function useData(): Data {
  // using temp dummy data set
  const data: GeoJson = uscities as GeoJson

  const [filterProperties, setFilterProperties] = useState<Filter>({
    property: "state_name",
    value: "",
    sliceMin: 0,
    sliceMax: 100
  })

  return useMemo(() => {
    const { property, value, sliceMin: lowCut, sliceMax: limit } = filterProperties

    let filteredFeatures: Feature[]
    if (value === "") {
      filteredFeatures = [] as Feature[]
    } else if (value === "all") {
      filteredFeatures = data.features
    } else {
      filteredFeatures = data.features.filter((d: Feature) => d.properties[property] === value)
    }

    const minimum = lowCut || 0
    const maximum = limit || lowCut + 50

    return {
      features: filteredFeatures.slice(minimum, maximum),
      filter: filterProperties,
      setFilterProperties
    }
  }, [filterProperties])
}
