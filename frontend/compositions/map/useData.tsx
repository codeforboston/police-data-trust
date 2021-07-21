//@ts-nocheck
import { useEffect, useState } from "react"
import uscities from "./uscities.json"

export default function useData() {
  // temp dummy data set
  const data = uscities

  const [filterProperties, setFilterProperties] = useState({ property: "population", value: 10000 })

  const [filteredData, setFilteredData] = useState(data)

  useEffect(() => {
    const { property, value } = filterProperties

    setFilteredData({
      ...data,
      features: data.features.filter((d) => d.properties[property] > value),
    })
  }, [filterProperties])

  return {
    data: filteredData,
    filter: filterProperties,
    setFilterProperties: setFilterProperties,
  }
}
