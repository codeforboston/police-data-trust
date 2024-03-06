import { request, AccessToken } from "../base"
import {
  User,
  RegisterRequest,
  LoginRequest,
  ForgotPassword,
  ResetPasswordRequest,
  ResetPasswordResponse,
  WhoamiRequest
} from "./types"

export function login(data: LoginRequest): Promise<AccessToken> {
  return request({
    url: "/auth/login",
    method: "POST",
    data
  }).then(({ access_token }) => access_token)
}

export function register(data: RegisterRequest): Promise<AccessToken> {
  return request({
    url: "/auth/register",
    method: "POST",
    data
  }).then(({ access_token }) => access_token)
}

export function forgotPassowrd(data: ForgotPassword): Promise<void> {
  return request({
    url: "/auth/forgotPassword",
    method: "POST",
    data
  })
}

export function resetPassword(req: ResetPasswordRequest): Promise<ResetPasswordResponse> {
  const { accessToken } = req

  return request({
    url: `/auth/resetPassword`,
    method: "POST",
    data: { password: req.password },
    accessToken
  })
}

export function whoami({ accessToken }: WhoamiRequest): Promise<User> {
  return request({
    url: "/auth/whoami",
    method: "GET",
    accessToken
  }).then(({ active, email, email_confirmed_at, first_name, last_name, phone_number, role }) => ({
    active,
    email,
    emailConfirmedAt: email_confirmed_at,
    firstName: first_name,
    lastName: last_name,
    phoneNumber: phone_number,
    role: role
  }))
}
