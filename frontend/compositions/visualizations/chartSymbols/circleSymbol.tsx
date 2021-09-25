import { ChartSymbolProps } from "../utilities/chartTypes"

export default function Circle(props: ChartSymbolProps) {
  const { location, size, color } = props

  return (
    <svg viewBox={`0 0 20 20`} height={size} width={size}>
      <circle cx={size / 2} cy={size / 2} r={size / 2} fill={color} />
    </svg>
  )
}
