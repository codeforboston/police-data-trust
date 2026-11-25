import React from "react"
import { afterEach, describe, expect, it, vi } from "vitest"
import { cleanup, render, screen } from "@testing-library/react"
import SearchResults from "@/components/search/SearchResults"
import { hasActiveFilters, parseSearchState } from "@/providers/SearchProvider"
import { SearchResponse } from "@/utils/api"
import { hasNoExactMatch, noResultsMessage } from "@/utils/noResults"

vi.mock("@/components/search/SearchResultsTabs", () => ({ default: () => null }))

const result = (title: string, exact_match: boolean | null): SearchResponse => ({
  uid: title,
  title,
  subtitle: "Officer at the Example Agency",
  content_type: "Officer",
  source: "Example Source",
  last_updated: "2026-01-01",
  exact_match
})

const partials = [result("Christopher Western", false), result("Brian West", false)]

const NO_EXACT = "No results found for Christopher West. Try a new search term."

afterEach(cleanup)

describe("noResultsMessage", () => {
  it("names the search term and the next step", () => {
    expect(noResultsMessage("Christopher West", false)).toBe(NO_EXACT)
    expect(noResultsMessage(" Christopher   West. ", true)).toBe(
      "No results found for Christopher West. Clear filters and try again."
    )
  })

  it("leaves the term out when only filters were used", () => {
    expect(noResultsMessage("", true)).toBe("No results found. Clear filters and try again.")
  })
})

describe("hasNoExactMatch", () => {
  it("is true only when every result is a partial match", () => {
    expect(hasNoExactMatch(partials)).toBe(true)
    expect(hasNoExactMatch([result("Christopher West", true), ...partials])).toBe(false)
    expect(hasNoExactMatch([result("Christopher West", null)])).toBe(false)
    expect(hasNoExactMatch([])).toBe(false)
  })
})

describe("SearchResults", () => {
  it("puts the message, then the line, then the count above partial matches", () => {
    render(
      <SearchResults tab="all" total={5000} results={partials} term="Christopher West" searched />
    )

    const message = screen.getByText(NO_EXACT)
    const line = screen.getByRole("separator")
    const count = screen.getByText("5000 results")
    const firstResult = screen.getByText("Christopher Western")

    const follows = (a: Node, b: Node) =>
      Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING)
    expect(follows(message, line)).toBe(true)
    expect(follows(line, count)).toBe(true)
    expect(follows(count, firstResult)).toBe(true)
  })

  it("asks to clear filters when filters are on", () => {
    render(
      <SearchResults
        tab="all"
        total={2}
        results={partials}
        term="Christopher West"
        hasFilters
        searched
      />
    )

    expect(
      screen.getByText("No results found for Christopher West. Clear filters and try again.")
    ).toBeTruthy()
  })

  it("shows no message or line when there are exact matches", () => {
    render(
      <SearchResults
        tab="all"
        total={5002}
        results={[result("Christopher West", true), ...partials]}
        term="Christopher West"
        searched
      />
    )

    expect(screen.queryByText(NO_EXACT)).toBeNull()
    expect(screen.queryByRole("separator")).toBeNull()
    expect(screen.getByText("5002 results")).toBeTruthy()
  })

  it("shows the message on the first page only", () => {
    render(
      <SearchResults
        tab="all"
        total={5000}
        results={partials}
        term="Christopher West"
        page={2}
        searched
      />
    )

    expect(screen.queryByText(NO_EXACT)).toBeNull()
    expect(screen.getByText("5000 results")).toBeTruthy()
  })

  it("shows only the message when nothing matches", () => {
    render(<SearchResults tab="all" total={0} results={[]} term="Qzxvplorth" searched />)

    expect(screen.getByText("No results found for Qzxvplorth. Try a new search term.")).toBeTruthy()
    expect(screen.queryByText("0 results")).toBeNull()
    expect(screen.queryByRole("separator")).toBeNull()
  })

  it("shows the filters message when only filters found nothing", () => {
    render(<SearchResults tab="agencies" total={0} results={[]} hasFilters searched />)

    expect(screen.getByText("No results found. Clear filters and try again.")).toBeTruthy()
  })
})

describe("hasActiveFilters", () => {
  const stateFor = (query: string) => parseSearchState(new URLSearchParams(query))

  it("counts the filters each tab sends", () => {
    expect(hasActiveFilters(stateFor("term=West"))).toBe(false)
    expect(hasActiveFilters(stateFor("term=West&state=MA"))).toBe(true)
    expect(hasActiveFilters(stateFor("term=West&tab=officers&ethnicity=Asian"))).toBe(true)
    expect(hasActiveFilters(stateFor("term=West&tab=agencies&jurisdiction=STATE"))).toBe(true)
  })

  it("ignores filters the current tab does not use", () => {
    expect(hasActiveFilters(stateFor("term=West&ethnicity=Asian"))).toBe(false)
    expect(hasActiveFilters(stateFor("term=West&tab=officers&jurisdiction=STATE"))).toBe(false)
  })
})
