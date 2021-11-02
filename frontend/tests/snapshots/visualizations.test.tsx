import * as React from "react"
import { Map } from "../../compositions"
import { render, router, setAuthForTest, userEvent, waitFor } from "../test-utils"

it("renders Map correctly", async () => {
  const { container, findByTitle } = render(<Map />)
  await expect(findByTitle("US Map")).resolves.toBeInTheDocument()
  expect(container).toMatchSnapshot()
})
