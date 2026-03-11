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
      dragPan: false,   // lock click-and-drag panning
      scrollZoom: true, // allow mouse wheel zoom
      doubleClickZoom: true,
      touchZoomRotate: true,
    })

    // Optional: keep pinch zoom on touch, but prevent touch rotation
    map.touchZoomRotate.disableRotation()

    const marker = new Marker()
      .setLngLat(center)
      .addTo(map)

    mapRef.current = map
    markerRef.current = marker

    return () => {
      markerRef.current?.remove()
      mapRef.current?.remove()
      markerRef.current = null
      mapRef.current = null
    }
  }, [])

  useEffect(() => {
    if (!mapRef.current || !markerRef.current) return

    mapRef.current.setCenter(center)
    mapRef.current.setZoom(zoom)
    markerRef.current.setLngLat(center)
  }, [center, zoom])

  return (
    <div
      ref={mapContainerRef}
      style={{ width: "100%", height: "300px" }}
    />
  )
}