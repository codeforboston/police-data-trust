import { BaseType, ScaleLinear, Selection, Transition } from "d3"
import { CityProperties } from "../../../models/visualizations"

export interface Coord {
  x: number
  y: number
}
export type Pair<T> = [T, T]
export type Path = string

export type Range = Pair<number>
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
  | "none"

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

export type ChartSymbolProps = Partial<ChartSymbolAttributes>

export interface PackableObj extends Partial<CityProperties> {
  name?: string
  children?: CityProperties | PackableObj[]
}

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
  symbol: "circle" | "square",
  title?: string
}

export type JoinSelection = Selection<SVGElement, DataPoint, BaseType, any>
export type JoinTransition = Transition<SVGElement, DataPoint, BaseType, any>
