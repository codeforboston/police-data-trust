import { geoAlbersUsa } from "d3"
import { Feature, FeatureCollection } from "geojson"
import { useSearch } from "../../../helpers"
import { Incident } from "../../../helpers/api"

export default function useSearchData() {
  const { incidentResults } = useSearch()
  const projection = geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])

  const createFeature = (incident: Incident) => {
    const feature: Feature = {
      type: "Feature",
      properties: { ...incident, locationLonLat: projection(incident.locationLonLat) },
      geometry: { type: "Point", coordinates: projection(incident.locationLonLat) }
    }
    return feature
  }

  const features: Feature[] = incidentResults?.results
    ? incidentResults.results
        .filter((incident) => incident.locationLonLat)
        .map((incident) => {
          return createFeature(incident)
        })
    : []

  return {
    type: "FeatureCollection",
    features: features
  } as FeatureCollection
}
