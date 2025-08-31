import { useState } from "react"
import { useRouter } from "next/navigation"
import type { UserData } from "@/types/user"
import { useAuth } from "@/providers/AuthProvider"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"

const useLogin = () => {
  const { setAccessToken, setRefreshToken } = useAuth()
  const [showPassword, setShowPassword] = useState(false)
  const [userData, setUserData] = useState<UserData>({
    email: "",
    firstname: "",
    lastname: "",
    phone: "",
    password: "",
    password2: ""
  })
  const [formError, setFormError] = useState(false)
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setUserData({ ...userData, [e.target.id]: e.target.value })
  }

  // return a boolean instead of setting state synchronously (avoids stale state)
  const isValid = (data: UserData) => {
    if (!data.email || !data.email.includes("@")) return false
    if (!data.password) return false
    return true
  }

  const coerceTokens = (payload: any) => {
    const accessToken =
      payload?.accessToken ?? payload?.access_token ?? null
    const refreshToken =
      payload?.refreshToken ?? payload?.refresh_token ?? null
    return { accessToken, refreshToken }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    const ok = isValid(userData)
    setFormError(!ok)
    if (!ok) {
      console.error("Form validation failed.")
      return
    }

    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.login}`

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: userData.email, password: userData.password })
      })

      if (!response.ok) {
        setFormError(true)
        return
      }

      const json = await response.json()
      const { accessToken, refreshToken } = coerceTokens(json)

      if (!accessToken || !refreshToken) {
        console.warn("Login succeeded but tokens missing from response:", json)
        setFormError(true)
        return
      }

      // Persist via AuthProvider (also writes to localStorage per your provider)
      setAccessToken(accessToken)
      setRefreshToken(refreshToken)

      router.push("/")
    } catch (error) {
      console.error("An error with login occurred:", error)
      setFormError(true)
    }
  }

  const handleClickShowPassword = () => setShowPassword((show) => !show)
  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => event.preventDefault()
  const handleMouseUpPassword = (event: React.MouseEvent<HTMLButtonElement>) => event.preventDefault()

  return {
    userData,
    handleChange,
    handleSubmit,
    showPassword,
    handleClickShowPassword,
    handleMouseDownPassword,
    handleMouseUpPassword,
    formError
  }
}

export default useLogin
