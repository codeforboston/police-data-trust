import * as React from "react"
import Dashboard from "../../pages/dashboard"
import renderer from "react-test-renderer"

it("renders Dashboard correctly", () => {
  const tree = renderer.create(<Dashboard />).toJSON()
  expect(tree).toMatchSnapshot()
})
