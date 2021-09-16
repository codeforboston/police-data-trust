import * as React from "react"
import { ProfileType } from "../../compositions/profile-content"
import renderer from "react-test-renderer"
import {users} from "../../models/mock-data"


it("renders Profile: Account Type panel with regular Viewer user", () => {
  const user = users[0]
  const tree = renderer.create(<ProfileType userData={user} />)
  expect(tree).toMatchSnapshot()
})

it("renders Profile: Account Type panel with Passport user", () => {
  const user = users[1]
  const tree = renderer.create(<ProfileType userData={user} />)
  expect(tree).toMatchSnapshot()
})