import { Coord } from "../utilities/chartTypes"
import styles from "./map.module.css"

export interface MarkerDescription {
  geoCenter: Coord
  dataPoint: number
  label: string
}

export interface MarkerLayerProps {
  markersData: MarkerDescription[]
}

export function MarkerLayer(props: MarkerLayerProps) {
  const { markersData } = props
  return (
    <svg viewBox="0, 0, 1200, 700" className={styles.markerLayer} height={"100%"} width={"100%"}>
      {markersData &&
        markersData.map((c, i) => {
          return <CircleMarker markerDescription={c} key={`${i}${c.dataPoint}`} />
        })}
    </svg>
  )
}

export interface CircleMarkerProps {
  markerDescription: MarkerDescription
}

export function CircleMarker(props: CircleMarkerProps) {
  const { markerDescription: c } = props
  return (
    <circle
      className={styles.circleMarker}
      cx={c.geoCenter.x}
      cy={c.geoCenter.y}
      r={c.dataPoint}
      onClick={() => console.log(c.label)}
    />
  )
}
