"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";

const TOKEN_NAME = "access_token";

type AuthContextType = {
  isLoggedIn: boolean;
  token: string | null;
  setAuthToken: (token: string) => void;
  removeAuthToken: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = window.localStorage.getItem(TOKEN_NAME);
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const setAuthToken = (newToken: string) => {
    setToken(newToken);
    window.localStorage.setItem(TOKEN_NAME, newToken);
  };

  const removeAuthToken = () => {
    setToken(null);
    window.localStorage.removeItem(TOKEN_NAME);
  };

  const isLoggedIn = !!token;

  return (
    <AuthContext.Provider value={{ isLoggedIn, token, setAuthToken, removeAuthToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};