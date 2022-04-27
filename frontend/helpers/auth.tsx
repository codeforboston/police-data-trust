import { useRouter } from "next/router"
import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"
import * as api from "./api"
import * as storage from "./storage"

const STORAGE_KEYS = {
  ACCESS_TOKEN: "__pdt_access_token__",
  USER: "__pdt_user__"
}

interface AuthState {
  accessToken?: api.AccessToken
  user?: api.User
  login: (credentials: api.LoginCredentials) => Promise<void>
  logout: () => Promise<void>
  register: (newUser: api.NewUser) => Promise<void>
}

export const AuthContext = createContext<AuthState>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const auth = useAuthenticationHook()
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}

/**
 * Renders the given component if authenticated, otherwise redirects to login.
 */
export function requireAuth(Component: () => JSX.Element) {
  return function ProtectedRoute() {
    const { user } = useAuth()
    const router = useRouter()
    const login = "/login"

    useEffect(() => {
      if (!user && router.pathname !== login) {
        router.push(login)
      }
    })

    return user ? <Component /> : null
  }
}

/** Redirects to the given route once the user is authenticated */
export function useRedirectOnAuth(route: string) {
  const { user } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (user && router.pathname !== route) {
      router.push(route)
    }
  })
}

function useAuthenticationHook(): AuthState {
  const {
    value: accessToken,
    set: setToken,
    clear: clearToken
  } = usePersistence<api.AccessToken>(STORAGE_KEYS.ACCESS_TOKEN)

  const {
    value: user,
    set: setUser,
    clear: clearUser
  } = usePersistence<api.User>(STORAGE_KEYS.USER)

  const login = useCallback(
    async (credentials: api.LoginCredentials) => {
      const accessToken = await api.login(credentials)
      const user = await api.whoami({ accessToken })
      setToken(accessToken)
      setUser(user)
    },
    [setToken, setUser]
  )

  const register = useCallback(
    async (newUser: api.NewUser) => {
      const accessToken = await api.register(newUser)
      const user = await api.whoami({ accessToken })
      setToken(accessToken)
      setUser(user)
    },
    [setToken, setUser]
  )

  const logout = useCallback(async () => {
    clearToken()
    clearUser()
  }, [clearToken, clearUser])

  return useMemo(
    () => ({ accessToken, user, login, register, logout }),
    [accessToken, login, logout, register, user]
  )
}

function usePersistence<T>(storageKey: string) {
  const [value, setValueState] = useState<T>(() => storage.getItem(storageKey))
  const set = useCallback(
      (v: T) => {
        storage.setItem(storageKey, v)
        setValueState(v)
      },
      [storageKey]
    ),
    clear = useCallback(() => {
      storage.removeItem(storageKey)
      setValueState(null)
    }, [storageKey])
  return {
    value,
    set,
    clear
  }
}

/**
 * Seeds auth values for test environments.
 */
export function setAuthForTest(
  user: api.User = {
    active: true,
    email: "testemail@example.com",
    firstName: "FirstTest",
    lastName: "LastTest",
    role: "Public"
  },
  accessToken: api.AccessToken = "faketoken"
) {
  storage.setItem(STORAGE_KEYS.USER, user)
  storage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken)
}

export function clearAuthForTest() {
  storage.removeItem(STORAGE_KEYS.USER)
  storage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
}
