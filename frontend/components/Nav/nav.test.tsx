import Nav from "./nav"
import { resetAuth, setAuthRefresh } from "@/utils/authState"
import { vi, expect, test, afterEach } from "vitest"
import { cleanup, render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"

// Mock useRouter before importing components that use it
vi.mock("next/navigation", () => {
  return {
    useRouter: () => ({
      push: vi.fn()
    }),
    usePathname: () => "/mock-path"
  }
})

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
  unmount()
})

test("Nav renders the Profile button and Logout menu item when logged in", async () => {
  const { unmount } = customRender(true)
  const user = userEvent.setup()

  const profileButton = screen.getByTestId("profile-button")
  expect(profileButton).toBeDefined()

  // Click profile button to open menu
  await user.click(profileButton)

  const logoutMenuItem = await screen.findByRole("menuitem", { name: /logout/i })
  expect(logoutMenuItem).toBeDefined()

  unmount()
})
