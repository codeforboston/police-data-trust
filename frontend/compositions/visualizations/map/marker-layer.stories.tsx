import { ComponentMeta, ComponentStory } from "@storybook/react"
import { geoAlbersUsa } from "d3-geo"
import React, { useMemo } from "react"
import { Coord } from "../utilities/chartTypes"
import { MarkerDescription, MarkerLayer } from "./marker-layer"

export default {
  title: "Visualizations/MarkerLayer",
  component: MarkerLayer
} as ComponentMeta<typeof MarkerLayer>

const Template: ComponentStory<typeof MarkerLayer> = (args) => <MarkerLayer {...args} />

export const Default = Template.bind({})

const projection = geoAlbersUsa()
  .scale(1300)
  .translate([487.5 + 112, 305 + 50])

const points = [
  [-87.6974962, 41.6928005] as [number, number],
  [-87.628557, 41.751667] as [number, number],
  [-87.5667172, 41.7642916] as [number, number]
]

const markersData: MarkerDescription[] = points.map((pt) => {
  const point = projection(pt)
  const geoCenter = {
    x: point[0],
    y: point[1]
  } as Coord

  const markerDescription: MarkerDescription = {
    geoCenter: geoCenter,
    dataPoint: 14,
    label: "marker"
  }

  return markerDescription
})

Default.args = {
  markersData: markersData
}
