import { useState } from "react";
import { redirect } from "next/navigation";
import type { UserData } from "@/app/types/user";
import { setAuthToken } from "@/app/utils/auth"
import API_ROUTES, { apiBaseUrl } from "@/app/utils/apiRoutes";

const useLogin = () => {
  const [showPassword, setShowPassword] = useState(false);

  const [userData, setUserData] = useState<UserData>({
    email: "",
    firstname: "",
    lastname: "",
    phone: "",
    password: "",
    password2: "",
  });

  const [formError, setFormError] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setUserData({ ...userData, [e.target.id]: e.target.value });
  };

  const handleFormError = (data: UserData) => {
    if (data.email == "" || !data.email.includes("@")) {
      setFormError(true);
      return;
    }

    if (data.password === "") {
      setFormError(true);
    } else {
      setFormError(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form submitted:", userData);
    handleFormError(userData);

    if (formError) {
      console.error("Form validation failed.");
      return;
    }

    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.login}`;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: userData.email,
          password: userData.password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAuthToken(data.token);
        redirect("/");
        
      } else {
        const errorData = await response.json();
        console.error("Login failed:", errorData.message);
      }
    } catch (error) {
      console.error("An error with login occurred:", error);
    }
  };

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    event.preventDefault();
  };

  return {
    userData,
    handleChange,
    handleSubmit,
    showPassword,
    handleClickShowPassword,
    handleMouseDownPassword,
    handleMouseUpPassword,
    formError,
  };
}

export default useLogin;