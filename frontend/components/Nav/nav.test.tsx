import Nav from "./nav"
import { expect, test } from "vitest"
import { render, screen } from "@testing-library/react"

test("Nav renders the logo and title", () => {
  render(<Nav />)
  expect(screen.getByAltText("Logo")).toBeDefined()
  expect(screen.getByText("National Police Data Coalition"))
})

// Test: renders the Feedback link
test("Nav renders the Feedback link", () => {
  expect(screen.getByRole("link", { name: /feedback/i }))
})

// Test: renders navigation links
test("Nav renders navigation links", () => {
  expect(screen.getByText("Home"))
  expect(screen.getByText("Data Explorer"))
  expect(screen.getByText("Community"))
  expect(screen.getByText("Collection"))
  expect(screen.getByText("Login"))
  expect(screen.getByText("Logout"))
})
