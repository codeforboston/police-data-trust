import { DataPoint } from "../utilities/chartTypes"

export function Bubble(props: DataPoint) {
  const { shape, r, coord, fill, stroke, strokeWidth } = props
  if (shape !== "circle") throw "shape must be circle"
  const { x, y } = coord
  return <circle r={r} cx={x} cy={y} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />
}
