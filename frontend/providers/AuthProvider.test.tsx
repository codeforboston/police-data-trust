import { vi, expect, test, beforeEach, afterEach } from "vitest"
import { renderHook, act, waitFor } from "@testing-library/react"
import { AuthProvider, useAuth } from "@/providers/AuthProvider"
import { resetAuth, getAuth } from "@/utils/authState"
import { ReactNode } from "react"

beforeEach(() => {
  localStorage.clear()
  resetAuth()
})

afterEach(() => {
  vi.restoreAllMocks()
})

const renderUseAuth = () => {
  // renderHook lets you test hooks in context
  return renderHook(() => useAuth(), {
    wrapper: ({ children }: { children: ReactNode }) => <AuthProvider>{children}</AuthProvider>
  })
}

test("hydrates tokens from localStorage", () => {
  localStorage.setItem("access_token", "abc123")
  localStorage.setItem("refresh_token", "xyz789")

  const { result } = renderUseAuth()
  expect(result.current.accessToken).toBe("abc123")
  expect(result.current.isLoggedIn).toBe(true)
})

test("setAccessToken updates localStorage and authState", () => {
  const { result } = renderUseAuth()

  act(() => result.current.setAccessToken("newToken"))

  expect(localStorage.getItem("access_token")).toBe("newToken")
  expect(getAuth().accessToken).toBe("newToken")
})

test("setAccessToken(null) clears token", () => {
  const { result } = renderUseAuth()

  act(() => result.current.setAccessToken("temp"))
  act(() => result.current.setAccessToken(null))

  expect(localStorage.getItem("access_token")).toBeNull()
  expect(getAuth().accessToken).toBeNull()
  expect(result.current.isLoggedIn).toBe(false)
})

test("logout clears both tokens", () => {
  const { result } = renderUseAuth()

  act(() => result.current.setAccessToken("temp"))
  act(() => result.current.setRefreshToken("tempRefresh"))
  act(() => result.current.logout())

  expect(localStorage.getItem("access_token")).toBeNull()
  expect(localStorage.getItem("refresh_token")).toBeNull()
  expect(result.current.isLoggedIn).toBe(false)
})

test("refreshAccessToken handles failed response", async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: false
  })

  const { result } = renderUseAuth()
  act(() => result.current.setRefreshToken("badRefresh"))

  const token = await result.current.refreshAccessToken()
  expect(token).toBeNull()
  expect(result.current.accessToken).toBeNull()
})

test("refreshAccessToken succeeds with new token", async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      access_token: "refreshed-token",
      expires_in: 86400
    })
  })

  const { result } = renderHook(() => useAuth(), {
    wrapper: ({ children }: { children: ReactNode }) => <AuthProvider>{children}</AuthProvider>
  })
  act(() => {
    result.current.setRefreshToken("goodRefresh")
  })

  await waitFor(() => {
    expect(result.current.refreshToken).toBe("goodRefresh")
  })
  const token = await result.current.refreshAccessToken()

  expect(token).toBe("refreshed-token")
  await waitFor(() => {
    expect(result.current.accessToken).toBe("refreshed-token")
  })
  expect(localStorage.getItem("access_token")).toBe("refreshed-token")
  expect(getAuth().accessToken).toBe("refreshed-token")
  expect(result.current.isLoggedIn).toBe(true)
})
