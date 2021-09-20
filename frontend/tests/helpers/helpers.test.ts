import { capitalizeFirstChar, getTitleCaseFromCamel } from "../../helpers"

test("handles empty string", () => {
  expect(capitalizeFirstChar("")).toBe("")
})

test("capitalizes first char", () => {
  expect(capitalizeFirstChar("word")).toBe("Word")
})

test("adds spaces and converts to title case", () => {
  expect(getTitleCaseFromCamel("desertWanderer")).toBe("Desert Wanderer")

  expect(getTitleCaseFromCamel("eatenByAnOstritch")).toBe("Eaten By An Ostritch")
})
