import { BaseType, ScaleLinear, Selection, Transition } from "d3"
import { CityProperties } from "../map/useData"

export interface Coord {
  x: number
  y: number
}

export type Pair<T> = [T, T]
export type Range = [number, number]
export type ColorTheme = (t: number) => string
export type ColorScale = ScaleLinear<number, number, never>

export type Angle = number

export type Position =
  | "top"
  | "right"
  | "bottom"
  | "left"
  | "top right"
  | "bottom right"
  | "top left"
  | "bottom left"

export interface ChartSymbolAttributes {
  label: string
  labelPosition: string
  data: { [name: string]: any }
  location: Coord
  offsetSize: number
  offsetDirection: Angle | "up" | "right" | "down" | "left"
  size: number
  color: string
}

export interface PackableObj extends Partial<CityProperties> {
  name?: string
  children?: CityProperties | PackableObj[]
}

export type Path = string

export interface DataPoint {
  shape: "circle" | "square" | Path
  value: number
  coord: Coord
  r: number
  fill?: string
  stroke?: string
  strokeWidth?: number
  label?: string
}
export type ChartSymbolProps = Partial<ChartSymbolAttributes>

export interface KeyItemProps {
  label?: string
  labelPosition?: Position
  symbol: "circle" | "square"
  color: string
  size?: number
}

export interface GradientKeyItemProps {
  lowLabel: string
  highLabel: string
  colorTheme: ColorTheme
  colorScale: ColorScale
  range: Range
  symbol: "circle" | "square"
}

export type JoinSelection = Selection<SVGElement, DataPoint, BaseType, any>
export type JoinTransition = Transition<SVGElement, DataPoint, BaseType, any>
