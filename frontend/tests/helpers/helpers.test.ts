import { capitalizeFirstChar, getTitleCaseFromCamel } from "../../helpers/syntax-helper"

test("capitalizes first char", () => {
  expect(capitalizeFirstChar("word")).toBe("Word")
})

test("getTitleCaseFromCamel", () => {
  expect(getTitleCaseFromCamel("desertWanderer")).toBe("Desert Wanderer")

  expect(getTitleCaseFromCamel("eatenByAnOstritch")).toBe("Eaten By An Ostritch")
})
