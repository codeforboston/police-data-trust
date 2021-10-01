import React from "react"
import { ComponentMeta } from "@storybook/react"
import UserLogin from "."

export default {
  title: "Pages/Login",
  component: UserLogin
} as ComponentMeta<typeof UserLogin>

export const Login = <UserLogin />

