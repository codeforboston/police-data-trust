import { FeatureCollection } from "geojson"
import { useEffect, useState } from "react"
import * as topojson from "topojson-client"
import { presimplify, simplify } from "topojson-simplify"
import { Topology } from "topojson-specification"

export function useBoundaryPaths(): FeatureCollection {
  const wholeTopo = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"
  const stateOnlyTopo = "https://cdn.jsdelivr.net/npm/us-atlas@3.0.0/states-10m.json"

  const [geoData, setGeoData] = useState<FeatureCollection>({
    type: "FeatureCollection",
    features: []
  })

  useEffect(
    () =>
      void fetch(stateOnlyTopo)
        .then((res) => res.json())
        .then((topology?: Topology) => {
          if (!topology) return

          topology = presimplify(topology)
          topology = simplify(topology, 0.05)

          const statesTopo = topojson.feature(
            topology,
            topology.objects.states
          ) as FeatureCollection
          return statesTopo
        })
        .then(setGeoData),
    [setGeoData]
  )
  return geoData
}
