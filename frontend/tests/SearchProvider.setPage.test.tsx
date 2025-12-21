import React from "react"
import { vi, describe, it, expect, beforeEach } from "vitest"
import { render, act, waitFor } from "@testing-library/react"
import { SearchProvider, useSearch } from "@/providers/SearchProvider"

// Mock next/navigation
// Mock next/navigation with stable mocks
const mockPush = vi.fn()
const mockSearchParams = new URLSearchParams("query=test&location=here&page=1")
vi.mock("next/navigation", async () => {
  return {
    useRouter: () => ({ push: mockPush }),
    useSearchParams: () => mockSearchParams
  }
})

// Mock apiFetch
vi.mock("@/utils/apiFetch", () => ({
  apiFetch: vi.fn(async () => ({
    ok: true,
    json: async () => ({ page: 2, pages: 3, per_page: 10, total: 30, results: [] })
  }))
}))

// Mock useAuth so SearchProvider has an accessToken
// Mock useAuth so SearchProvider has an accessToken (stable object)
const mockRefresh = vi.fn()
const mockAuth = { accessToken: "token", refreshAccessToken: mockRefresh }
vi.mock("@/providers/AuthProvider", async () => {
  return {
    useAuth: () => mockAuth
  }
})

const Consumer = () => {
  const { setPage } = useSearch()
  React.useEffect(() => {
    ;(async () => {
      await setPage(2)
    })()
  }, [setPage])
  return <div>consumer</div>
}

describe("SearchProvider setPage", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("fetches new page and updates history", async () => {
    const { container, unmount } = render(
      <SearchProvider>
        <Consumer />
      </SearchProvider>
    )

    // Wait until router.push is called with the expected page param
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalled()
    })

    // Inspect last call arg
    const lastArg = mockPush.mock.calls[mockPush.mock.calls.length - 1][0]
    expect(lastArg).toMatch(/page=2/)

    // cleanup to avoid leftover timers/effects
    unmount()
    await act(async () => Promise.resolve())
  })
})
