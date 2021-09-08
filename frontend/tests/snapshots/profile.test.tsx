import * as React from "react"
import Profile from "../../pages/profile"
import renderer from "react-test-renderer"

it("renders Profile Page correctly", () => {
  const tree = renderer.create(<Profile />).toJSON()
  expect(tree).toMatchSnapshot()
})
