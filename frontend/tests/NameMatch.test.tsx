import { describe, expect, it } from "vitest"
import { rankByName, tokenizeSearch } from "@/utils/nameMatch"

const rank = (names: string[], term: string) =>
  rankByName(names, term, (name) => name).map(({ item, exact_match }) => [item, exact_match])

describe("tokenizeSearch", () => {
  it("splits words like the server does", () => {
    // Same case as backend/tests/test_name_search.py.
    expect(tokenizeSearch("Rivera, Anthony J. O'Brien-Smith AND (x)")).toEqual([
      "rivera",
      "anthony",
      "j",
      "o'brien",
      "smith",
      "x"
    ])
    expect(tokenizeSearch("Rivera' ")).toEqual(["rivera"])
    expect(tokenizeSearch("( OR )")).toEqual([])
  })
})

describe("rankByName", () => {
  const units = ["Narcotics Division", "Bronx Narcotics", "Bronx Vice", "Brooklyn North"]

  it("counts whole words in any order as exact and lists them first", () => {
    expect(rank(units, "narcotics bronx")).toEqual([
      ["Bronx Narcotics", true],
      ["Bronx Vice", false],
      ["Narcotics Division", false]
    ])
  })

  it("treats word starts as partial matches", () => {
    expect(rank(units, "Bro")).toEqual([
      ["Bronx Narcotics", false],
      ["Bronx Vice", false],
      ["Brooklyn North", false]
    ])
  })

  it("puts names made only of the searched words first", () => {
    expect(rank(["Bronx Narcotics Task Force", "Bronx Narcotics"], "Bronx Narcotics")).toEqual([
      ["Bronx Narcotics", true],
      ["Bronx Narcotics Task Force", true]
    ])
  })

  it("leaves out names that match no searched word", () => {
    expect(rank(units, "Queens")).toEqual([])
  })
})
