import React from "react"
import { vi, describe, it, expect, beforeEach } from "vitest"
import { render, act, waitFor } from "@testing-library/react"
import {
  SearchProvider,
  buildApiParams,
  parseSearchState,
  useSearch
} from "@/providers/SearchProvider"

const mockPush = vi.fn()
const mockSearchParams = new URLSearchParams(
  "term=test&city=Albany%2C%20NY&city_uid=city-1&source=CAPStat&source_uid=source-1&page=1"
)

vi.mock("next/navigation", async () => {
  return {
    useRouter: () => ({ push: mockPush }),
    useSearchParams: () => mockSearchParams
  }
})

vi.mock("@/utils/apiFetch", () => ({
  apiFetch: vi.fn(async () => ({
    ok: true,
    json: async () => ({ page: 2, pages: 3, per_page: 10, total: 30, results: [] })
  }))
}))

const mockRefresh = vi.fn()
const mockAuth = { accessToken: "token", hasHydrated: true, refreshAccessToken: mockRefresh }

vi.mock("@/providers/AuthProvider", async () => {
  return {
    useAuth: () => mockAuth
  }
})

const PaginationConsumer = () => {
  const { setPage } = useSearch()

  React.useEffect(() => {
    setPage(2)
  }, [setPage])

  return <div>consumer</div>
}

const FilterConsumer = () => {
  const { setFilters } = useSearch()

  React.useEffect(() => {
    setFilters({
      city: ["Albany, NY", "Buffalo, NY"],
      cityUid: ["city-1", "city-2"],
      source: ["CAPStat", "50.org"],
      sourceUid: ["source-1", "source-2"]
    })
  }, [setFilters])

  return <div>filters</div>
}

describe("SearchProvider", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("parses repeated city and source params", () => {
    const state = parseSearchState(mockSearchParams)

    expect(state.city).toEqual(["Albany, NY"])
    expect(state.cityUid).toEqual(["city-1"])
    expect(state.state).toEqual([])
    expect(state.jurisdiction).toEqual([])
    expect(state.agency).toEqual([])
    expect(state.agencyUid).toEqual([])
    expect(state.ethnicity).toEqual([])
    expect(state.source).toEqual(["CAPStat"])
    expect(state.sourceUid).toEqual(["source-1"])
  })

  it("fetches new page and updates history", async () => {
    const { unmount } = render(
      <SearchProvider>
        <PaginationConsumer />
      </SearchProvider>
    )

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalled()
    })

    const lastArg = mockPush.mock.calls[mockPush.mock.calls.length - 1][0]
    expect(lastArg).toMatch(/page=2/)

    unmount()
    await act(async () => Promise.resolve())
  })

  it("stores multi-select filters as repeated params", async () => {
    render(
      <SearchProvider>
        <FilterConsumer />
      </SearchProvider>
    )

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalled()
    })

    const lastArg = mockPush.mock.calls[mockPush.mock.calls.length - 1][0]
    expect(lastArg).toContain("city=Albany%2C+NY")
    expect(lastArg).toContain("city=Buffalo%2C+NY")
    expect(lastArg).toContain("city_uid=city-1")
    expect(lastArg).toContain("city_uid=city-2")
    expect(lastArg).toContain("source=CAPStat")
    expect(lastArg).toContain("source=50.org")
    expect(lastArg).toContain("source_uid=source-1")
    expect(lastArg).toContain("source_uid=source-2")
  })

  it("builds all-tab API params with repeated filter values", () => {
    const params = buildApiParams({
      term: "john",
      tab: "all",
      page: 2,
      state: [],
      jurisdiction: [],
      agency: [],
      agencyUid: [],
      ethnicity: [],
      city: ["Albany, NY", "Buffalo, NY"],
      cityUid: ["city-1", "city-2"],
      source: ["CAPStat"],
      sourceUid: ["source-1"]
    }).toString()

    expect(params).toContain("term=john")
    expect(params).toContain("page=2")
    expect(params).toContain("city=Albany%2C+NY")
    expect(params).toContain("city=Buffalo%2C+NY")
    expect(params).toContain("city_uid=city-1")
    expect(params).toContain("city_uid=city-2")
    expect(params).toContain("source=CAPStat")
    expect(params).toContain("source_uid=source-1")
  })
})
