export type MarkerDescription = {
  geoCenter: [number, number]
  dataPoint: number
  label: string
}

export type MarkerLayerProps = {
  markersData: MarkerDescription[]
}

export function MarkerLayer(props: MarkerLayerProps) {
  const { markersData } = props
  return (
    <svg viewBox="0, 0, 1200, 700" className="marker-layer" height={"100%"} width={"100%"}>
      {markersData && markersData.map((c, i) => {
        return <CircleMarker markerDescription={c} key={`${i}${c.dataPoint}`} />
      })}
    </svg>
  )
}

export type CircleMarkerProps = {
  markerDescription: MarkerDescription
}

export function CircleMarker(props: CircleMarkerProps) {
  const { markerDescription: c } = props
  return (
    <circle
      className="circle-marker"
      cx={c.geoCenter[0]}
      cy={c.geoCenter[1]}
      r={c.dataPoint}
      onClick={() => console.log(c.label)}
    />
  )
}
