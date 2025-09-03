import { getAuth } from "@/utils/authState"
import { ApiError } from "./apiError"

let refreshPromise: Promise<string | null> | null = null

export async function apiFetch(url: string, init: RequestInit = {}): Promise<Response> {
  const { accessToken, refreshAccessToken, logout } = getAuth()
  if (!accessToken) {
    const newTok = await refreshAccessToken()
    if (!newTok) {
      logout?.()
      throw new ApiError("No access token", "NO_ACCESS_TOKEN", 401)
    }
    return fetch(new Request(url, withAuth(init, newTok)))
  }

  let res = await fetch(new Request(url, withAuth(init, accessToken)))

  if (res.status === 401) {
    console.log("Access token expired, refreshing...")
    if (!refreshPromise) {
      refreshPromise = refreshAccessToken().finally(() => {
        refreshPromise = null
      })
    }
    const newTok = await refreshPromise
    if (!newTok) {
      logout?.()
      throw new ApiError("No access token", "NO_ACCESS_TOKEN", 401)
    }
    res = await fetch(new Request(url, withAuth(init, newTok)))
    if (res.status === 401) logout?.()
  }

  return res
}

function withAuth(init: RequestInit, token: string): RequestInit {
  const headers = new Headers(init.headers)
  if (!headers.has("Authorization")) headers.set("Authorization", `Bearer ${token}`)
  if (typeof FormData !== "undefined" && init.body instanceof FormData)
    headers.delete("Content-Type")
  return { ...init, headers }
}
