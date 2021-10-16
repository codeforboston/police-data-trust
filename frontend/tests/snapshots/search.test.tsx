import * as React from "react"
import Dashboard from "../../pages/search"
import { render, router, setAuthForTest, userEvent, waitFor } from "../test-utils"

jest.mock("../../compositions/visualizations/map")

beforeAll(() => setAuthForTest())

it("renders Dashboard correctly", async () => {
  // Ensure consistent title id's for fontawesome
  jest.spyOn(global.Math, "random").mockImplementation(() => 0)
  const { container } = render(<Dashboard />)
  expect(container).toMatchSnapshot()
  jest.clearAllMocks
})

it("navigates to logout page", async () => {
  const { getByRole } = render(<Dashboard />)
  const logout = getByRole("menuitem", { name: /sign out/i })

  userEvent.click(logout)

  await waitFor(() => expect(router.pathname).toBe("/logout"))
})
