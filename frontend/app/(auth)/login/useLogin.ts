import { useState } from "react"
import { useRouter } from "next/navigation"
import type { UserData } from "@/types/user"
import { useAuth } from "@/providers/AuthProvider"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"

const useLogin = () => {
  const { setAuthToken } = useAuth()
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

  const handleFormError = (data: UserData) => {
    if (data.email == "" || !data.email.includes("@")) {
      setFormError(true)
      return
    }

    if (data.password === "") {
      setFormError(true)
    } else {
      setFormError(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    handleFormError(userData)

    if (formError) {
      console.error("Form validation failed.")
      return
    }

    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.login}`

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: userData.email,
          password: userData.password
        })
      })

      if (response.ok) {
        const data = await response.json()
        setAuthToken(data.access_token)
        router.push("/")
      } else {
        setFormError(true)
      }
    } catch (error) {
      setFormError(true)
      console.error("An error with login occurred:", error)
    }
  }

  const handleClickShowPassword = () => setShowPassword((show) => !show)

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
  }

  const handleMouseUpPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
  }

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
