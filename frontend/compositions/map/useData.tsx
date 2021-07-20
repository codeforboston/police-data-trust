//@ts-nocheck
import fetch from "node-fetch"
import { useEffect, useState } from "react"
import { filter } from "topojson"
import * as topojson from "topojson-client"
import uscities from "./uscities.json"

export default function useData(property, value) {
  const data = uscities
  // const data = fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json")

  // console.log(uscities)
  const [filterProperties, setFilterProperties] = useState({ property: "population", value: 10000 })

  const [filteredData, setFilteredData] = useState(data)


  useEffect(() => {

    // console.log(filterProperties)
    
    const { property, value } = filterProperties
    
    setFilteredData({
      ...data,
      features: data.features.filter((d) => {
        const points = d.properties[filterProperties.property] > filterProperties.value
        return points
      }),
    })
  }, [filterProperties])

  return { data: filteredData, filter: filterProperties, setFilterProperties: setFilterProperties }
}
