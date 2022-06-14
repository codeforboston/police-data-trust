import { useEffect, useRef } from "react"
import { Loader } from "@googlemaps/js-api-loader"

import { Incident } from "../../../helpers/incident"
import styles from "./incident-view-header.module.css"

export default function IncidentViewHeader(incident: Incident) {
  const { id, stop_type, time_of_incident, location } = incident
  const { wrapper, idAndStop, data, category, stopType } = styles

  const date = time_of_incident.toDateString()
  const time = time_of_incident.toTimeString()

  const displayLocation = useRef(null)

  useEffect(() => {
    const loader = new Loader({
      apiKey: process.env.NEXT_PUBLIC_MAPS_KEY,
      version: "weekly"
    })

    loader.load().then(() => {
      const geocoder = new google.maps.Geocoder()
      const mapLocation = { lat: location.latitude, lng: location.longitude }

      geocoder
        .geocode({
          location: mapLocation
        })
        .then((res) => {
          displayLocation.current.innerText = res.results[0]
            ? res.results[0].formatted_address
            : "N/A"
        })
    })
  })

  return (
    <div className={wrapper}>
      <div className={idAndStop}>
        <strong>{id}</strong>
        <p className={stopType}>{stop_type}</p>
      </div>
      <div className={data}>
        <p className={category}>Date</p>
        <p>{date}</p>
      </div>
      <div className={data}>
        <p className={category}>Time</p>
        <p>{time}</p>
      </div>
      <div className={data}>
        <p className={category}>Location</p>
        <p ref={displayLocation}></p>
      </div>
    </div>
  )
}
