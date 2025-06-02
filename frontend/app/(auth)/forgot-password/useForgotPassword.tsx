import { useState } from "react";
import API_ROUTES, { apiBaseUrl } from "@/app/utils/apiRoutes";
import { redirect } from "next/navigation"

const useResetPassword = () => {
  const [formError, setFormError] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");

  const handleFormError = (email: string) => {
    if (email === "" || !email.includes("@")) {
      setFormError(true);
      return;
    }
    setFormError(false);
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleFormError(email);

    if (formError) {
      console.error("Form validation failed.");
      return;
    }

    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.forgotPassword}`;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        redirect("/auth/reset-password/success");
      } else {
        const errorData = await response.json();
        console.error("Error sending password reset email:", errorData);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
    setEmail(""); // Clear the email field after submission
    setFormError(false); // Reset form error state
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setEmail(e.target.value);
  }

  return {
    handleSubmit,
    handleChange,
    formError,
    email
  }
}

export default useResetPassword;