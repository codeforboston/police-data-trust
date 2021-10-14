import React from "react"
import { lightBlueGrey, lightDarkBlueTheme } from "../utilities"
import { ChartKey, GradientKeyItem, scaleDataToColorTheme, SymbolKeyItem } from "../chart-key"

export default function MapKey(props: { title: string }) {
  const colorScale = scaleDataToColorTheme(0, 1000)
  const { title } = props
  const chartKeyElements: JSX.Element[] = [
    <SymbolKeyItem
      label="Data Rich Cities"
      key={title}
      labelPosition={"right"}
      color={"var(--darkBlue)"}
      symbol={"circle"}
      size={20}
    />,
    <SymbolKeyItem
      key={title}
      label="Data Poor Cities"
      labelPosition={"right"}
      color={"var(--lightBlue)"}
      symbol={"square"}
      size={20}
    />,
    <GradientKeyItem
      key={title}
      symbol="square"
      colorTheme={lightDarkBlueTheme}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel="Less Data"
      highLabel="More Data"
    />,
    <GradientKeyItem
      key={title}
      symbol="circle"
      colorTheme={lightBlueGrey}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel="Blue"
      highLabel="Grey"
    />
  ]

  return (
    <div style={{ position: "absolute", right: 0, bottom: 0 }}>
      <ChartKey title={title} entries={chartKeyElements} position={"none"} />
    </div>
  )
}
