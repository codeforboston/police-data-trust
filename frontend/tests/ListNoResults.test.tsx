import React from "react"
import { afterEach, describe, expect, it, vi } from "vitest"
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react"
import OfficerList from "@/components/Details/OfficerList"
import UnitList from "@/components/Details/UnitList"
import { Agency, Officer, Unit } from "@/utils/api"
import { DEFAULT_OFFICER_LIST_FILTERS, OfficerListFilters } from "@/hooks/useOfficerListFilters"

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }))

const agency = { uid: "agency-1", name: "Example Agency", hq_state: "NY" } as Agency

const officer = (first: string, last: string, exact_match: boolean | null) =>
  ({ uid: `${first}-${last}`, first_name: first, last_name: last, exact_match }) as Officer

const renderOfficers = (officers: Officer[], filters: Partial<OfficerListFilters>) =>
  render(
    <OfficerList
      org={agency}
      orgType="agency"
      officers={officers}
      filters={{ ...DEFAULT_OFFICER_LIST_FILTERS, ...filters }}
      filterMode="hybrid"
    />
  )

afterEach(cleanup)

describe("Officer list", () => {
  it("shows the message and line above partial matches", () => {
    renderOfficers([officer("Christopher", "Western", false)], {
      searchTerm: "Christopher West"
    })

    expect(
      screen.getByText("No results found for Christopher West. Try a new search term.")
    ).toBeTruthy()
    expect(screen.getByRole("separator")).toBeTruthy()
  })

  it("asks to clear filters when a filter is on", () => {
    renderOfficers([officer("Christopher", "Western", false)], {
      searchTerm: "Christopher West",
      rank: ["Captain"]
    })

    expect(
      screen.getByText("No results found for Christopher West. Clear filters and try again.")
    ).toBeTruthy()
  })

  it("shows nothing extra when there is an exact match", () => {
    renderOfficers(
      [officer("Christopher", "West", true), officer("Christopher", "Western", false)],
      { searchTerm: "Christopher West" }
    )

    expect(screen.queryByRole("status")).toBeNull()
    expect(screen.queryByRole("separator")).toBeNull()
  })

  it("puts the message in the empty table", () => {
    renderOfficers([], { searchTerm: "Qzxvplorth" })

    const table = screen.getByRole("table")
    expect(
      within(table).getByText("No results found for Qzxvplorth. Try a new search term.")
    ).toBeTruthy()
    expect(screen.queryByRole("separator")).toBeNull()
  })

  it("keeps the plain empty text when nothing was searched", () => {
    renderOfficers([], {})

    expect(screen.getByText("No officers found.")).toBeTruthy()
  })
})

describe("Unit list", () => {
  const units = ["Bronx Narcotics", "Bronx Vice", "Narcotics Division"].map(
    (name) => ({ uid: name, name }) as Unit
  )

  const search = (text: string) => {
    render(<UnitList agency={agency} units={units} />)
    fireEvent.change(screen.getByPlaceholderText("search unit or try anything"), {
      target: { value: text }
    })
  }

  const rowNames = () =>
    within(screen.getByRole("table"))
      .getAllByRole("row")
      .slice(1)
      .map((row) => row.textContent)

  it("finds units whose name has the words in any order, exact matches first", () => {
    search("narcotics bronx")

    expect(rowNames()).toEqual(["Bronx Narcotics", "Bronx Vice", "Narcotics Division"])
    expect(screen.queryByRole("separator")).toBeNull()
  })

  it("shows the message and line when only partial matches are found", () => {
    search("Narc")

    expect(screen.getByText("No results found for Narc. Try a new search term.")).toBeTruthy()
    expect(screen.getByRole("separator")).toBeTruthy()
    expect(rowNames()).toEqual(["Bronx Narcotics", "Narcotics Division"])
  })

  it("shows only the message when no unit matches", () => {
    search("Queens")

    expect(rowNames()).toEqual(["No results found for Queens. Try a new search term."])
    expect(screen.queryByRole("separator")).toBeNull()
  })
})
