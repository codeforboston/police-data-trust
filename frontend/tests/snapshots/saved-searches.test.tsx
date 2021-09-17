import * as React from "react"
import { SavedSearches } from "../../compositions/profile-content"
import renderer from "react-test-renderer"

it("renders Saved Searches page correctly", () => {
  const tree = renderer.create(<SavedSearches />).toJSON()
  expect(tree).toMatchSnapshot()
})