import * as React from "react"
import Dashboard from "../../pages/search"
import { render, router, setAuthForTest, userEvent, waitFor } from "../test-utils"

beforeAll(() => setAuthForTest())

it("renders Dashboard correctly", async () => {
  const { container } = render(<Dashboard />)
  expect(container).toMatchSnapshot()
})

it("redirects to login on logout", async () => {
  const { getByRole } = render(<Dashboard />)
  const logout = getByRole("button", { name: /logout/i })

  userEvent.click(logout)

  await waitFor(() => expect(router.pathname).toBe("/login"))
})
