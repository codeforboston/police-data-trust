import * as React from "react"
import Home from "../../pages/index"
import renderer from "react-test-renderer"

it("renders Home correctly", () => {
  const tree = renderer.create(<Home />).toJSON()
  expect(tree).toMatchSnapshot()
})
