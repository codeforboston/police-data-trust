export type ApiErrorCode =
  | "NO_ACCESS_TOKEN"
  | "UNAUTHORIZED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "NETWORK"
  | "TIMEOUT"
  | "BAD_RESPONSE"
  | "UNKNOWN"

export class ApiError extends Error {
  readonly code: ApiErrorCode
  readonly status?: number
  readonly details?: unknown

  constructor(message: string, code: ApiErrorCode, status?: number, details?: unknown) {
    super(message)
    this.name = "ApiError"
    this.code = code
    this.status = status
    this.details = details
  }
}

export const isApiError = (e: unknown): e is ApiError => e instanceof ApiError
