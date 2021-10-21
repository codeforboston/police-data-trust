import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import BaseMap, { getFakeData } from "./BaseMap"
import { geoAlbersUsa } from "d3-geo"

export default {
  title: "Visualizations/BaseMap",
  component: BaseMap
} as ComponentMeta<typeof BaseMap>

const Template: ComponentStory<typeof BaseMap> = (args) => <BaseMap {...args} />

const data = getFakeData()

export const Default = Template.bind({})

Default.args = {
  data: data,
  projection: geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])
}