import axiosModule, { AxiosRequestConfig } from "axios"

export type AccessToken = string

export interface User {
  active: boolean
  email: string
  emailConfirmedAt?: string
  firstName?: string
  lastName?: string
}

export interface NewUser {
  email: string
  password: string
  firstName?: string
  lastName?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

interface AuthenticatedRequest {
  accessToken: AccessToken
}

export type RegisterRequest = NewUser
export type LoginRequest = LoginCredentials
export type WhoamiRequest = AuthenticatedRequest

const axios = axiosModule.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000/api/v1",
  timeout: 5000
})

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

export function whoami({ accessToken }: WhoamiRequest): Promise<User> {
  return request({
    url: "/auth/test",
    method: "GET",
    accessToken
  }).then(({ active, email, email_confirmed_at, first_name, last_name }) => ({
    active,
    email,
    emailConfirmedAt: email_confirmed_at,
    firstName: first_name,
    lastName: last_name
  }))
}

function request({ accessToken, ...config }: AxiosRequestConfig & { accessToken?: AccessToken }) {
  let { headers, ...rest } = config
  if (accessToken) {
    headers = {
      Authorization: `Bearer ${accessToken}`,
      ...headers
    }
  }

  return axios({
    headers,
    ...rest
  }).then((response) => response.data)
}
