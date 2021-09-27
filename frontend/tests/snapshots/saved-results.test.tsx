import * as React from "react"
import { SavedResults } from "../../compositions/profile-content"
import renderer from "react-test-renderer"

it("renders Saved Results page correctly", () => {
  const tree = renderer.create(<SavedResults />).toJSON()
  expect(tree).toMatchSnapshot()
})
