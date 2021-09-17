import * as React from "react"
import renderer from "react-test-renderer"
import {
  RegistrationResponse,
  PassportApplicationResponse
} from "../../compositions/enrollment-response/enrollment-response"

it("renders Register:Success correctly", () => {
  const tree = renderer.create(<RegistrationResponse success />).toJSON()
  expect(tree).toMatchSnapshot()
}),
  it("renders Register:Fail correctly", () => {
    const tree = renderer.create(<RegistrationResponse />).toJSON()
    expect(tree).toMatchSnapshot()
  })

it("renders Passport:Success correctly", () => {
  const tree = renderer.create(<PassportApplicationResponse success />).toJSON()
  expect(tree).toMatchSnapshot()
})

it("renders Passport:Fail correctly", () => {
  const tree = renderer.create(<PassportApplicationResponse />).toJSON()
  expect(tree).toMatchSnapshot()
})
