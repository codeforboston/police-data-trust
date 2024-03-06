import { AuthenticatedRequest } from "../base"

export interface User {
  active: boolean
  role: string
  email: string
  emailConfirmedAt?: string
  firstName?: string
  lastName?: string
  phoneNumber?: string
}

export interface NewUser {
  email: string
  password: string
  firstName?: string
  lastName?: string
  phoneNumber?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface ForgotPassword {
  email: string
}

export interface ResetPasswordRequest extends AuthenticatedRequest {
  accessToken: string
  password: string
}

export interface ResetPasswordResponse {
  message: string
}

export type RegisterRequest = NewUser
export type LoginRequest = LoginCredentials
export type WhoamiRequest = AuthenticatedRequest
