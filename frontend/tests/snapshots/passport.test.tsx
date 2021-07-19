import * as React from "react"
import renderer from "react-test-renderer"
import Passport from "../../pages/apply/index"

it("renders correctly", () => {
  const tree = renderer.create(<Passport />).toJSON()
  expect(tree).toMatchSnapshot()
})
