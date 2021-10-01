import * as React from "react"
import { SavedResults } from "../../compositions"
import { render } from "../test-utils"

it("renders Saved Results page correctly", () => {
  const { container } = render(<SavedResults />)
  expect(container).toMatchSnapshot()
})
