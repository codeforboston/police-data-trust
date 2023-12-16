import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import BubbleChart from "./BubbleChart"

export default {
  title: "Visualizations/BubbleChart",
  component: BubbleChart
} as ComponentMeta<typeof BubbleChart>

const Template: ComponentStory<typeof BubbleChart> = () => <BubbleChart height={500} />

export const Default = Template.bind({})
