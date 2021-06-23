import * as React from "react"
import Register from "../../pages/register"
import renderer from "react-test-renderer"

it("renders Register correctly", () => {
  const tree = renderer.create(<Register />).toJSON()
  expect(tree).toMatchSnapshot()
})
