import * as React from "react"
import Dashboard from "../../pages/search"
import { render, router, setAuthForTest, userEvent, waitFor } from "../test-utils"

jest.mock('../../compositions/visualizations/map')

beforeAll(() => setAuthForTest())

it("renders Dashboard correctly", async () => {
  const { container } = render(<Dashboard />)
  expect(container).toMatchSnapshot()
})

it("navigates to logout page", async () => {
  const { getByRole } = render(<Dashboard />)
  const logout = getByRole("menuitem", { name: /sign out/i })

  userEvent.click(logout)

  await waitFor(() => expect(router.pathname).toBe("/logout"))
})
