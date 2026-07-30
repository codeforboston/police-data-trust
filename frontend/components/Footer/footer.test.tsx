import Footer from "."
import { cleanup, render, screen } from "@testing-library/react"
import { afterEach, expect, test } from "vitest"

afterEach(() => {
  cleanup()
})

test("Footer shows the same public contact details without nonprofit verification fields", () => {
  render(<Footer />)

  const contactSection = screen.getByLabelText("Contact details")

  expect(screen.getByText("National Police Data Coalition")).toBeDefined()
  expect(contactSection.textContent).toContain("4201 Main St")
  expect(contactSection.textContent).toContain("Houston, TX 77002")
  expect(screen.getByRole("link", { name: "info@nationalpolicedata.org" })).toBeDefined()

  expect(screen.queryByText("87-4427926")).toBeNull()
  expect(screen.queryByText("The Ion")).toBeNull()
  expect(
    screen.queryByText(/establishing the first nationally integrated, independent repository/i)
  ).toBeNull()
})
