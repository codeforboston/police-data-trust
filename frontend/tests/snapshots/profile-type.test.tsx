import * as React from "react"
import { ProfileType } from "../../compositions"
import { MockProfileType } from "../../compositions/profile-type"
import { render } from "../test-utils"

it("renders Profile: Account Type panel with current user", () => {
  const { container } = render(<ProfileType />)
  expect(container).toMatchSnapshot()
})

it("renders Profile: Account Type panel with Passport user", () => {
  const passportUser = {
    active: true,
    firstName: "Passport",
    lastName: "User",
    email: "passport.user@email.com",
    phone: "9995559999",
    role: 1
  }
  const { container } = render(<MockProfileType {...passportUser} />)
  expect(container).toMatchSnapshot()
})
