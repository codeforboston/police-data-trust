import * as React from "react"
import About from "../../pages/about"
import renderer from "react-test-renderer"

it("randers About Page correctly", () => {
  const tree = renderer.create(<About />).toJSON()
  expect(tree).toMatchSnapshot()
})
