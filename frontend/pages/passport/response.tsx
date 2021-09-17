import * as React from "react"
import { Layout } from "../../shared-components"
import { PassportApplicationResponse, ResponseProps } from "../../compositions/enrollment-response/enrollment-response"

export default function Response(props: ResponseProps) {
  const wrapper = {
    width: "60%",
    margin: "20vh auto"
  }

  return (
    <Layout>
      <div style={wrapper}>
        <PassportApplicationResponse {...props} />
      </div>
      
    </Layout>
  )
}