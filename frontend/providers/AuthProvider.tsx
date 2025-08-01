"use client"
import { createContext, useContext, useState, useEffect, ReactNode } from "react"

const TOKEN_NAME = "access_token"

type AuthContextType = {
  isLoggedIn: boolean
  accessToken: string | null
  setAuthToken: (accessToken: string) => void
  removeAuthToken: () => void
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = window.localStorage.getItem(TOKEN_NAME)
    if (storedToken) {
      setAccessToken(storedToken)
    }
  }, [])

  const setAuthToken = (newToken: string) => {
    setAccessToken(newToken)
    window.localStorage.setItem(TOKEN_NAME, newToken)
  }

  const removeAuthToken = () => {
    setAccessToken(null)
    window.localStorage.removeItem(TOKEN_NAME)
  }

  const isLoggedIn = !!accessToken

  return (
    <AuthContext.Provider value={{ isLoggedIn, accessToken, setAuthToken, removeAuthToken }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
