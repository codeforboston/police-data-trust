"use client";
import { useState } from "react";
import { UserData } from "@/types/user";
import { useAuth } from "@/context/AuthProvider";
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useRouter } from "next/navigation";

const useRegister = () => {
  const { setAuthToken } = useAuth();
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
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserData({ ...userData, [e.target.id]: e.target.value });
  };

  const handleFormError = (data: UserData) => {
    if (data.firstname == "" || data.lastname == "") {
      setFormError(true);
      return;
    }

    if (data.email == "" || !data.email.includes("@")) {
      setFormError(true);
      return;
    }

    if (data.password != data.password2) {
      setFormError(true);
      return;
    }

    if (data.phone === "") {
      setFormError(true);
      return;
    }
    
    if (data.password === "" || data.password2 === "") {
      setFormError(true);
    } else {
      setFormError(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => { 
    e.preventDefault()

    handleFormError(userData);
    const apiUrl = `${apiBaseUrl}${API_ROUTES.auth.register}`;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: userData.email,
          password: userData.password,
          firstname: userData.firstname,
          lastname: userData.lastname,
          phone_number: userData.phone,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAuthToken(data.access_token);
        router.push("/register/success");
      } else {
        router.push("/register/error");
      }
    } catch (error) {
      router.push("/register/error");
      console.error("An error occurred:", error);
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
    formError,
    showPassword,
    handleClickShowPassword,
    handleMouseDownPassword,
    handleMouseUpPassword,
  };
}

export default useRegister;