import { BaseType, D3ZoomEvent, ScaleLinear, Selection, Transition } from "d3"
import { Feature } from "geojson"
import { CityProperties } from "../../../models/visualizations"

export interface Coord {
  x: number
  y: number
}
export type Pair<T> = [T, T]
export type PointCoord = Pair<number>
export type BoundingType = [PointCoord, PointCoord]
export type D3CallableSelectionType = Selection<Element, unknown, any, any>
export type D3ZoomEventType = D3ZoomEvent<Element, any>

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

export type StateID = string

export type NodeData = {
  __data__: Feature
}
export type TargetWithData = EventTarget & NodeData & SVGElement
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
  symbol: "circle" | "square"
  title?: string
}

export type JoinSelection = Selection<SVGElement, DataPoint, BaseType, any>
export type JoinTransition = Transition<SVGElement, DataPoint, BaseType, any>
