"use client"

import { createContext, useContext, useState, useCallback, useEffect, ReactNode } from "react"
import { setAuthRefresh } from "@/utils/authState"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"

const ACCESS_TOKEN_KEY = "access_token"
const REFRESH_TOKEN_KEY = "refresh_token"

interface AuthContext {
  accessToken: string | null
  refreshToken: string | null
  isLoggedIn: boolean
  hasHydrated?: boolean
  setAccessToken: (token: string | null) => void
  setRefreshToken: (token: string | null) => void
  refreshAccessToken: () => Promise<string | null>
  logout: () => void
}

const Ctx = createContext<AuthContext | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, _setAccessToken] = useState<string | null>(null)
  const [refreshToken, _setRefreshToken] = useState<string | null>(null)
  const [hasHydrated, setHasHydrated] = useState(false)

  // --- persistence helpers ---
  const setAccessToken = useCallback((token: string | null) => {
    _setAccessToken(token)
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token)
    } else {
      localStorage.removeItem(ACCESS_TOKEN_KEY)
    }
  }, [])

  const setRefreshToken = useCallback((token: string | null) => {
    _setRefreshToken(token)
    if (token) {
      localStorage.setItem(REFRESH_TOKEN_KEY, token)
    } else {
      localStorage.removeItem(REFRESH_TOKEN_KEY)
    }
  }, [])

  // --- hydrate from localStorage on first mount (client only) ---
  useEffect(() => {
    try {
      const storedAccess = localStorage.getItem(ACCESS_TOKEN_KEY)
      const storedRefresh = localStorage.getItem(REFRESH_TOKEN_KEY)
      if (storedAccess) _setAccessToken(storedAccess)
      if (storedRefresh) _setRefreshToken(storedRefresh)
    } catch (e) {
      console.error("Error during auth hydration", e)
    } finally {
      setHasHydrated(true)
    }
  }, [])

  // --- core refresh function used by apiFetch ---
  const refreshAccessToken = useCallback(async (): Promise<string | null> => {
    if (!refreshToken) return null

    const response = await fetch(`${apiBaseUrl}${API_ROUTES.auth.refresh}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${refreshToken}`
      }
    })

    if (!response.ok) {
      console.error("Failed to refresh access token")
      // blow away tokens so the app can redirect to login
      setAccessToken(null)
      setRefreshToken(null)
      return null
    }

    const data = await response.json()
    if (!data?.access_token) {
      console.error("Refresh response missing access_token")
      setAccessToken(null)
      setRefreshToken(null)
      return null
    }

    setAccessToken(data.access_token)
    return data.access_token as string
  }, [refreshToken, setAccessToken, setRefreshToken])

  // --- publish current token + refresher to global apiFetch bridge ---
  useEffect(() => {
    if (!hasHydrated) return
    setAuthRefresh({ accessToken, refreshAccessToken })
  }, [accessToken, refreshAccessToken, hasHydrated])

  // --- preemptive refresh a bit before JWT expiry ---
  useEffect(() => {
    if (!accessToken) return
    const exp = getJwtExp(accessToken)
    if (!exp) return

    const nowMs = Date.now()
    const expMs = exp * 1000
    // refresh 30s before expiry (clamp to minimum of 0)
    const delay = Math.max(expMs - nowMs - 30_000, 0)

    const id = window.setTimeout(() => {
      // fire and forget; apiFetch will still handle 401s just in case
      console.log("Preemptively refreshing access token...")
      refreshAccessToken().catch(() => {})
    }, delay)

    return () => window.clearTimeout(id)
  }, [accessToken, refreshAccessToken])

  const logout = useCallback(() => {
    setAccessToken(null)
    setRefreshToken(null)
  }, [setAccessToken, setRefreshToken])

  const isLoggedIn = !!accessToken

  return (
    <Ctx.Provider
      value={{
        accessToken,
        refreshToken,
        isLoggedIn,
        hasHydrated,
        setAccessToken,
        setRefreshToken,
        refreshAccessToken,
        logout
      }}>
      {children}
    </Ctx.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider")
  return ctx
}

/** Safely parse a JWT's exp (seconds since epoch). Returns null on failure. */
function getJwtExp(token: string): number | null {
  const parts = token.split(".")
  if (parts.length !== 3) return null
  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/")
    const json = atob(base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "="))
    const payload = JSON.parse(json)
    return typeof payload?.exp === "number" ? payload.exp : null
  } catch {
    return null
  }
}
