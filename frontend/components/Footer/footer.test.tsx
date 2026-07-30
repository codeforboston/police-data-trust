import Footer from "."
import { ORGANIZATION_DETAILS } from "@/utils/constants"
import { cleanup, render, screen } from "@testing-library/react"
import { afterEach, expect, test } from "vitest"

afterEach(() => {
  cleanup()
})

test("Footer shows the same public contact details without nonprofit verification fields", () => {
  render(<Footer />)

  const contactSection = screen.getByLabelText("Contact details")
  const { address } = ORGANIZATION_DETAILS

  expect(screen.getByText(ORGANIZATION_DETAILS.name)).toBeDefined()
  expect(contactSection.textContent).toContain(address.street)
  expect(contactSection.textContent).toContain(address.suite)
  expect(contactSection.textContent).toContain(address.cityStateZip)
  expect(screen.getByRole("link", { name: ORGANIZATION_DETAILS.email })).toBeDefined()

  expect(screen.queryByText(ORGANIZATION_DETAILS.ein)).toBeNull()
  expect(screen.queryByText(ORGANIZATION_DETAILS.mission)).toBeNull()
})
