import React from "react"
import { lightBlueGrey, lightDarkBlueTheme } from "../utilities"
import { ChartKey, GradientKeyItem, scaleDataToColorTheme, SymbolKeyItem } from "../chart-key"

export default function MapKey(props: { title: string }) {
  const colorScale = scaleDataToColorTheme(0, 100)
  const { title } = props
  const chartKeyElements: JSX.Element[] = [
    <GradientKeyItem
      key={title}
      symbol="square"
      colorTheme={lightDarkBlueTheme}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel="minimum value"
      highLabel="maximum value"
    />
  ]

  return (
    <div style={{ position: "absolute", right: 0, bottom: 0 }}>
      <ChartKey title={title} entries={chartKeyElements} position={"none"} />
    </div>
  )
}
