import * as React from "react"
import Login from "../../pages/login"
import renderer from "react-test-renderer"

it("renders Login correctly", () => {
  const tree = renderer.create(<Login />).toJSON()
  expect(tree).toMatchSnapshot()
})
