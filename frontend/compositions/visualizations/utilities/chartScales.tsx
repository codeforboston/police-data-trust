import { interpolate, scaleLinear, scaleLog } from "d3"
import { ColorScale, ColorTheme, Pair } from "./chartTypes"

export const lightDarkBlueTheme = interpolate("#7caed7", "#303463")
export const greyBlueTheme = interpolate("#666666", "#303463")
export const lightBlueGrey = interpolate("#7caed7", "#666666")

export function steppedGradient(
  dataSteps: number[] | number,
  colorTheme: ColorTheme,
  colorScale: ColorScale
): string[] {
  const colorSteps: string[] = []
  if (typeof dataSteps === "number") {
    for (let i = 0; i <= dataSteps; i++) {
      colorSteps.push(colorTheme(i / dataSteps))
    }
  } else dataSteps.map((step) => colorTheme(colorScale(step)))

  return colorSteps
}

export function createColorScale(minMax: Pair<number>) {
  return scaleLinear().domain(minMax).range([0, 1])
}

export function createLogScale(minMax: Pair<number>) {
  return scaleLog().domain(minMax).range([0, 1])
}
