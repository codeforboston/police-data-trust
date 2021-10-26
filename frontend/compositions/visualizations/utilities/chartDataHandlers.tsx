import { descending, extent, hierarchy, HierarchyCircularNode, pack } from "d3"
import { Feature } from "geojson"
import { CityProperties } from "../../../models/visualizations"
import { createColorScale, createLogScale, lightDarkBlueTheme } from "./chartScales"
import { DataPoint, PackableObj } from "./chartTypes"

export function parseProperties(feature: Feature) {
  const properties = feature.properties as CityProperties
  const numZips: number[] = (properties.zips as string).split(" ").map((i) => Number(i))
  const isMilitary: boolean = (properties.military as string).match(/true/i) !== null
  const isIncorporated: boolean = (properties.incorporated as string).match(/true/i) !== null
  return {
    ...properties,
    zips: numZips,
    military: isMilitary,
    incorporated: isIncorporated
  }
}

export function packPop(data: PackableObj): HierarchyCircularNode<PackableObj> {
  return pack()
    .size([1000 - 2, 500 - 2])
    .padding(10)(
    hierarchy(data)
      .sum((d) => d.density)
      .sort((a, b) => a.value - b.value)
  )
}

export function formatDataToSymbolData(data: CityProperties[], shift: number) {
  if (!data) return []

  const root = packPop(formatPackProperties(data.slice(shift)) as PackableObj)

  const minMax = extent(root.leaves().map((l) => l.value))
  const scaleColor = createColorScale(minMax)

  const symbolPropsArray: DataPoint[] = root.leaves().map((leaf) => {
    return {
      shape: "circle",
      value: leaf.value,
      r: leaf.r,
      coord: { x: leaf.x, y: leaf.y },
      fill: lightDarkBlueTheme(scaleColor(leaf.value)),
      label: leaf.data.city
    }
  })

  return symbolPropsArray
}

export function formatPackProperties(
  data: CityProperties | CityProperties[]
): PackableObj | CityProperties {
  return Array.isArray(data)
    ? ({
        name: "cities",
        children: data.map((d) => formatPackProperties(d))
      } as PackableObj)
    : (data as CityProperties)
}
