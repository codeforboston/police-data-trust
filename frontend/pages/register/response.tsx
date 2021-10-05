import * as React from "react"
import { Layout } from "../../shared-components"
import { RegistrationResponse } from "../../compositions/enrollment-response/enrollment-response"

export default function Response() {
  const wrapper = {
    width: "60%",
    margin: "20vh auto"
  }
  return (
    <div style={wrapper}>
      <RegistrationResponse success={true} />
      <RegistrationResponse success={false} />
    </div>
  )
}
