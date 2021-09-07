import * as React from "react"
import Profile from "../../pages/profile"
import renderer from "react-test-renderer"

it("randers Profile Page correctly", () => {
  const tree = renderer.create(<Profile />).toJSON()
  expect(tree).toMatchSnapshot()
})
