import React from "react"
import { lightBlueGrey, lightDarkBlueTheme } from "../charts"
import ChartKey, {
  GradientKeyItem, scaleDataToColorTheme, SymbolKeyItem
} from "../charts/chartKey"

export default function MapKey(props: {}) {
  const colorScale = scaleDataToColorTheme(0, 1000)


  const chartKeyElements = [
    <SymbolKeyItem
      label="Data Rich Cities"
      labelPosition={"right"}
      color={"var(--darkBlue)"}
      symbol={"circle"}
      size={20}
    />,
    <SymbolKeyItem
      label="Data Poor Cities"
      labelPosition={"right"}
      color={"var(--lightBlue)"}
      symbol={"square"}
      size={20}
    />,
    <GradientKeyItem
      symbol="square"
      colorTheme={lightDarkBlueTheme}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel="Less Data"
      highLabel="More Data"
    />,
    <GradientKeyItem
      symbol="circle"
      colorTheme={lightBlueGrey}
      colorScale={colorScale}
      range={[0, 1000]}
      lowLabel="Blue"
      highLabel="Grey"
    />,
  ]

  return <ChartKey title="testKey" children={chartKeyElements} position={"bottom right"} />
}
