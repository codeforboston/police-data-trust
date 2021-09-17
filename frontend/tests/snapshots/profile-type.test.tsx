import * as React from "react"
import { ProfileType } from "../../compositions/profile-content"
import renderer from "react-test-renderer"

it("renders Profile: Account Type panel with regular Viewer user", () => {
  const publicUser = {
    id: 1,
    active: true,
    firstName: "Public",
    lastName: "User",
    email: "public.user@email.com",
    phone: "9995559999",
    role: 2
  }
  const tree = renderer.create(<ProfileType userData={publicUser} />)
  expect(tree).toMatchSnapshot()
})

it("renders Profile: Account Type panel with Passport user", () => {
  const passportUser = {
    id: 2,
    active: true,
    firstName: "Passport",
    lastName: "User",
    email: "passport.user@email.com",
    phone: "9995559999",
    role: 1
  }
  const tree = renderer.create(<ProfileType userData={passportUser} />)
  expect(tree).toMatchSnapshot()
})