import * as React from "react"
import { SavedSearches } from "../../compositions"
import { render } from "../test-utils"

it("renders Saved Results page correctly", () => {
  const { container } = render(<SavedSearches />)
  expect(container).toMatchSnapshot()
})
