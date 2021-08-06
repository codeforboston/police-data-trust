import * as React from 'react'
import renderer from "react-test-renderer"
import {
  RegistrationResponse,
  PassportApplicationResponse
} from '../../compositions/enrollment-response/enrollment-response'

it('renders Register:Success correctly', () => {
  const tree = renderer.create(<RegistrationResponse isSuccess />).toJSON()
  expect(tree).toMatchSnapshot()
})

it('renders Register:Fail correctly', () => {
  const tree = renderer.create(<RegistrationResponse isSuccess={false} />).toJSON()
  expect(tree).toMatchSnapshot()
})

it('renders Passport:Success correctly', () => {
  const tree = renderer.create(<PassportApplicationResponse isSuccess />).toJSON()
  expect(tree).toMatchSnapshot()
})

it('renders Passport:Fail correctly', () => {
  const tree = renderer.create(<PassportApplicationResponse isSuccess={false} />).toJSON()
  expect(tree).toMatchSnapshot()
})