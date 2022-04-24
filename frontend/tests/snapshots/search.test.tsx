import * as React from "react"
import { act } from "react-dom/test-utils"
import { DashboardHeader } from "../../compositions"
import { render, router, setAuthForTest, userEvent, waitFor } from "../test-utils"

jest.mock("../../compositions/visualizations/map")

beforeAll(() => setAuthForTest())

it("renders Dashboard correctly", async () => {
  const { container } = render(<DashboardHeader />)
  await waitFor(() => expect(container).toMatchSnapshot())
})

it("navigates to logout page", async () => {
  const { getByText } = render(<DashboardHeader />)
  const logout = getByText(/sign out/i)

  act(() => {
    userEvent.click(logout)
  })

  await waitFor(() => expect(router.pathname).toBe("/logout"))
})
