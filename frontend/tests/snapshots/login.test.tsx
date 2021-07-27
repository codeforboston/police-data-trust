import * as React from "react"
import UserLogin from "../../pages/login"
import renderer from "react-test-renderer"

it("renders Login correctly", () => {
  const tree = renderer.create(<UserLogin />).toJSON()
  expect(tree).toMatchSnapshot()
})
