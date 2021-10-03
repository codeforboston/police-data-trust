import * as React from "react"
import { LandingPage } from "../../compositions/"
import renderer from "react-test-renderer"

it("renders Saved Searches page correctly", () => {
  const tree = renderer.create(<LandingPage />).toJSON()
  expect(tree).toMatchSnapshot()
})
