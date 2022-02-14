import { Feature } from "geojson"
import { Incident } from "../../../helpers/api"
import { MarkerDescription } from "./marker-layer"
import useSearchData from "./useSearchData"

export default function useMarkerLayerSearchData() {
  const searchResults = useSearchData()

  return searchResults?.features.map((f: Feature) => {
    const { locationLonLat, id, department } = f.properties as Incident
    return {
      geoCenter: { x: locationLonLat[0], y: locationLonLat[1] },
      dataPoint: id,
      label: department
    } as MarkerDescription
  })
}
