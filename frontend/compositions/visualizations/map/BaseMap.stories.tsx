import { ComponentMeta, ComponentStory } from "@storybook/react"
import { geoAlbersUsa } from "d3-geo"
import { FeatureCollection } from "geojson"
import React from "react"
import BaseMap from "./BaseMap"

export default {
  title: "Visualizations/BaseMap",
  component: BaseMap
} as ComponentMeta<typeof BaseMap>

const Template: ComponentStory<typeof BaseMap> = (args) => <BaseMap {...args} />

export const Default = Template.bind({})

const geoData: FeatureCollection[] = []

Default.args = {
  geoData: geoData,
  projection: geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])
}
