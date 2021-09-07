import * as React from "react"
import DashboardHeader from "../../compositions/dashboard-header/dashboard-header"
import renderer from "react-test-renderer"

it("renders Dashboard Header correctly", () => {
  const tree = renderer.create(<DashboardHeader />).toJSON()
  expect(tree).toMatchSnapshot()
})
