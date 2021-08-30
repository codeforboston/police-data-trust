import { lightDarkBlueTheme, steppedGradient } from "./chartKey"

describe("chart key builders", () => {
  test("calculates stepped Gradient", () => {
    const stepG = steppedGradient(5, lightDarkBlueTheme)
    console.log(stepG)
  })
})
