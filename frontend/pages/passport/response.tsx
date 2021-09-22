import * as React from "react"
import { PassportApplicationResponse } from "../../compositions/enrollment-response/enrollment-response"

export default function Response() {
  const wrapper = {
    width: "60%",
    margin: "20vh auto"
  }

  return (
    <div style={wrapper}>
      <PassportApplicationResponse success={true} />
      <PassportApplicationResponse success={false} />
    </div>
  )
}
