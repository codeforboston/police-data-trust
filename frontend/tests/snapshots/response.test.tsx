import * as React from 'react'
import renderer, { act } from "react-test-renderer"
import {
  RegistrationResponse,
  PassportApplicationResponse
} from '../../compositions/enrollment-response/enrollment-response'

it('renders Register:Success correctly', () => {
  act(() => {
    const tree = renderer.create(<RegistrationResponse isSuccess />).toJSON()
    expect(tree).toMatchSnapshot()
  })
}),

it('renders Register:Fail correctly', () => {
  act(() => {
    const tree = renderer.create(<RegistrationResponse isSuccess={false} />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

it('renders Passport:Success correctly', () => {
  act(() => {
    const tree = renderer.create(<PassportApplicationResponse isSuccess />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})

it('renders Passport:Fail correctly', () => {
  act(() => {
    const tree = renderer.create(<PassportApplicationResponse isSuccess={false} />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})