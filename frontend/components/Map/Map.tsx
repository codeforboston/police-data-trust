import { Map, Marker } from "maplibre-gl"
import { useEffect, useRef } from "react"
import "maplibre-gl/dist/maplibre-gl.css"

type MapProps = {
  // [Longitude, Latitude]
  center: [number, number]
  zoom: number
}

export default function MapComponent({ center, zoom }: MapProps) {
  const mapContainerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<Map | null>(null)
  const markerRef = useRef<Marker | null>(null)

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return

    const map = new Map({
      container: mapContainerRef.current,
      style: "https://tiles.openfreemap.org/styles/bright",
      center,
      zoom,

      // disable panning / movement
      dragPan: false,
      dragRotate: false,
      keyboard: false,
      touchPitch: false,
      boxZoom: false,

      // allow zoom, but always around the map center
      scrollZoom: { around: "center" },
      touchZoomRotate: { around: "center" },
      doubleClickZoom: true,
    })

    map.touchZoomRotate.disableRotation()

    const marker = new Marker()
      .setLngLat(center)
      .addTo(map)

    mapRef.current = map
    markerRef.current = marker

    return () => {
      marker.remove()
      map.remove()
      markerRef.current = null
      mapRef.current = null
    }
  }, [])

  useEffect(() => {
    const map = mapRef.current
    const marker = markerRef.current
    if (!map || !marker) return

    map.setCenter(center)
    map.setZoom(zoom)
    marker.setLngLat(center)
  }, [center, zoom])

  return (
    <div
      ref={mapContainerRef}
      style={{ width: "100%", height: "300px" }}
    />
  )
}