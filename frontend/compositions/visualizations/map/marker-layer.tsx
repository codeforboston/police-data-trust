import { select } from "d3"
import { Coord } from "../utilities/chartTypes"
import styles from "./map.module.css"

export interface MarkerDescription {
  geoCenter: Coord
  dataPoint?: number
  label: string
}

export interface MarkerLayerProps {
  markersData: MarkerDescription[]
  type?: "circle" | "square"
  fill?: string
}

export function MarkerLayer(props: MarkerLayerProps) {
  const { markersData } = props

  const handleMouseOver = (event: MouseEvent, markerDescription: MarkerDescription) => {
    console.log("moue enter marker")

    const x = markerDescription.geoCenter.x + (event.target as HTMLElement).offsetLeft
    const y = markerDescription.geoCenter.y + (event.target as HTMLElement).offsetTop

    // popup.moveTo({x: x, y: y})
    // popup.setHeader(markerDescription.label)
    // popup.setBody("this is a marker popup")
    // popup.show()
  }

  const handleMouseMove = (event: MouseEvent) => {
    event.stopPropagation()
  }

  const handleMouseLeave = () => {
    console.log("mosue leave makrer")
    // popup.hide()
  }

  return (
    <svg
      viewBox="0, 0, 1200, 700"
      id={"marker-layer"}
      className={styles.markerLayer}
      height={"100%"}
      width={"100%"}>
      {markersData &&
        markersData.map((c, i) => {
          return (
            <>
              <Marker
                type={"circle"}
                markerDescription={c}
                key={`${i}${c.dataPoint}`}
                handleMouseOver={handleMouseOver}
                handleMouseLeave={handleMouseLeave}
                handleMouseMove={handleMouseMove}
              />
            </>
          )
        })}
    </svg>
  )
}

export interface MarkerProps {
  markerDescription: MarkerDescription
  mousePosition?: Coord
  handleMouseOver(event: any, markerDescription: MarkerDescription): void
  handleMouseLeave(): void
  handleMouseMove(event: any, markerDescription: MarkerDescription): void
  type?: "circle" | "square"
  transformScale?: number
}

export function Marker(props: MarkerProps) {
  const {
    type,
    markerDescription,
    handleMouseLeave,
    handleMouseMove,
    handleMouseOver,
    transformScale
  } = props

  const coordinate: Coord = markerDescription.geoCenter

  return (
    <g
      type={type}
      {...props}
      onClick={() => console.log(markerDescription.label)}
      onMouseOver={(e) => handleMouseOver(e, markerDescription)}
      onMouseMove={(e) => handleMouseMove(e, markerDescription)}
      onMouseOut={handleMouseLeave}>
      {type === "circle" && <CircleMarker position={coordinate} />}
      {type === "square" && <SquareMarker position={coordinate} />}
    </g>
  )
}

export function CircleMarker(props: { position: Coord; fill?: string }) {
  const {
    position: { x, y },
    fill
  } = props
  const r = 10
  const cx = x
  const cy = y

  return (
    <circle
      className={"marker " + styles.circleMarker}
      cx={cx}
      cy={cy}
      r={r}
      fill={fill || "var(--darkBlue)"}
    />
  )
}

export function SquareMarker(props: { position: Coord; fill?: string }) {
  const {
    position: { x, y },
    fill
  } = props
  const r = 20

  return (
    <rect
      className={"marker " + styles.squareMarker}
      x={x - r / 2}
      y={y - r / 2}
      width={r}
      height={r}
      fill={fill || "var(--darkBlue)"}
    />
  )
}
