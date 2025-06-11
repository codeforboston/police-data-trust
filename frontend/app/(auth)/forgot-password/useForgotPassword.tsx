import { useState } from "react"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { redirect } from "next/navigation"

const useResetPassword = () => {
  const [formError, setFormError] = useState<boolean>(false)
  const [email, setEmail] = useState<string>("")

  const handleFormError = (email: string) => {
    if (email === "" || !email.includes("@")) {
      setFormError(true)
      return
    }
    setFormError(false)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    handleFormError(email)

    if (formError) {
      console.error("Form validation failed.")
      return
    }

    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.forgotPassword}`

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email })
      })

      if (response.ok) {
        redirect("/reset-password/success")
      } else {
        setFormError(true)
        const errorData = await response.json()
        console.error("Error sending password reset email:", errorData)
      }
    } catch (error) {
      setFormError(true)
      console.error("Error sending password reset email:", error)
    }
    setEmail("") // Clear the email field after submission
    setFormError(false) // Reset form error state
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setEmail(e.target.value)
  }

  return {
    handleSubmit,
    handleChange,
    formError,
    email
  }
}

export default useResetPassword
