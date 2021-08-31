import React from "react"
import { ChartKey, GradientKeyItem, scaleDataToColorTheme } from "../chart-key"
import { lightDarkBlueTheme } from "../charts"
import { Pair } from "../charts/chartTypes"

export default function BubbleKey(props: { dataMaxMin: Pair<number> }) {
  const { dataMaxMin } = props
  const colorScale = scaleDataToColorTheme(0, 1000)
  const title = "bubble-key"

  const dataMinMaxKey = (
    <GradientKeyItem
      symbol="circle"
      colorTheme={lightDarkBlueTheme}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel={dataMaxMin[0] + ""}
      highLabel={dataMaxMin[1] + ""}
      title="population"
    />
  )
  const chartKeyElements: JSX.Element[] = [dataMinMaxKey]

  return <ChartKey title={title} position={"right"} entries={chartKeyElements} />
}
