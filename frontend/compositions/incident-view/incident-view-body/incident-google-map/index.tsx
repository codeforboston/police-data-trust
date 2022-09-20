import { useEffect, useRef } from "react"
import { Loader } from "@googlemaps/js-api-loader"
import type { Incident } from "../../../../helpers/api"
import styles from "./map.module.css"

export default function OverheadMap(incident: Incident) {
  const location = { lat: incident.latitude, lng: incident.longitude }
  const googleMap = useRef(null)

  useEffect(() => {
    const loader = new Loader({
      apiKey: process.env.NEXT_PUBLIC_MAPS_KEY,
      version: "weekly"
    })

    loader.load().then(() => {
      const map = new google.maps.Map(googleMap.current, {
        center: location,
        zoom: 8,
        fullscreenControl: false,
        streetViewControl: false,
        mapTypeControl: false
      })

      const marker = new google.maps.Marker({
        map: map,
        position: location
      })
    })
  })

  return <div id="map" className={styles.map} ref={googleMap}></div>
}
