import Nav from "./nav"
import { resetAuth, setAuthRefresh } from "@/utils/authState"
import { AuthProvider } from "@/providers/AuthProvider"
import { vi, expect, test, afterEach } from "vitest"
import { cleanup, render, screen } from "@testing-library/react"

const customRender = (isLoggedIn = false) => {
  setAuthRefresh({
    accessToken: isLoggedIn ? "fake-token" : null,
    refreshAccessToken: vi.fn(),
    logout: vi.fn()
  })
  return render(<Nav />)
}

afterEach(() => {
  cleanup()
  resetAuth()
})

test("Nav renders the logo and title", () => {
  const { unmount } = customRender()
  expect(screen.getByAltText("Logo")).toBeDefined()
  expect(screen.getByText("National Police Data Coalition"))
  unmount()
})

// Test: renders the Feedback link
test("Nav renders the Feedback link", () => {
  const { unmount } = customRender()
  expect(screen.getByRole("link", { name: /feedback/i })).toBeDefined()
  unmount()
})

// Test: renders navigation links
test("Nav renders navigation links", () => {
  const { unmount } = customRender()
  expect(screen.getByText("Home"))
  expect(screen.getByText("Data Explorer"))
  expect(screen.getByText("Community"))
  expect(screen.getByText("Collection"))
  expect(screen.getByText("Login"))
  unmount()
})

test("Nav renders the Logout link", () => {
  const { unmount } = customRender(true)
  screen.debug()
  expect(screen.getByText("Logout"))
  unmount()
})
