import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import BaseMap from "./BaseMap"
import { geoAlbersUsa } from "d3-geo"
import { FakeData } from "../utilities/chartTypes"

export default {
  title: "Visualizations/BaseMap",
  component: BaseMap
} as ComponentMeta<typeof BaseMap>

const Template: ComponentStory<typeof BaseMap> = (args) => <BaseMap {...args} />

export const Default = Template.bind({})

const data: FakeData[] = [
    {
      UID: 1,
      state: "04",
      value: 10
    },
    {
      UID: 2,
      state: "05",
      value: 30
    },
    {
      UID: 3,
      state: "06",
      value: 100
    },
    {
      UID: 4,
      state: "09",
      value: 70
    },
    {
      UID: 5,
      state: "10",
      value: 20
    },
    {
      UID: 6,
      state: "11",
      value: 10
    },
    {
      UID: 7,
      state: "12",
      value: 30
    },
    {
      UID: 8,
      state: "13",
      value: 100
    },
    {
      UID: 9,
      state: "14",
      value: 70
    },
    {
      UID: 10,
      state: "15",
      value: 20
    }
  ]

Default.args = {
  data: data,
  projection: geoAlbersUsa()
    .scale(1300)
    .translate([487.5 + 112, 305 + 50])
}