import * as React from "react"
import Logo from "../../shared-components/logo/logo"
import renderer from "react-test-renderer"

it("renders Logo correctly", () => {
  const tree = renderer.create(<Logo />).toJSON()
  expect(tree).toMatchSnapshot()
})
