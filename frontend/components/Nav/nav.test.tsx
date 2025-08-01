import Nav from "./nav"
import { vi, expect, test, afterEach } from "vitest"
import { cleanup, render, screen } from "@testing-library/react"
import { AuthContext } from "../../providers/AuthProvider" // Adjust the import path if needed

const accessToken = null
const setAuthToken = vi.fn()
const removeAuthToken = vi.fn()

const customRender = (isLoggedIn = false) => {
  return render(
    <AuthContext.Provider value={{ isLoggedIn, accessToken, setAuthToken, removeAuthToken }}>
      <Nav />
    </AuthContext.Provider>
  )
}

afterEach(() => {
  cleanup()
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
  expect(screen.getByText("Logout"))
  unmount()
})
