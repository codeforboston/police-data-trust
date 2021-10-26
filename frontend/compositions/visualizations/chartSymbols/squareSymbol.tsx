import { ChartSymbolProps } from "../utilities"

export default function Square(props: ChartSymbolProps) {
  const { color, size } = props

  return (
    <svg viewBox="0 0 20 20" width={size} height={size}>
      <rect height={size} width={size} fill={color}></rect>
    </svg>
  )
}
