"use client";
import { useState, useEffect } from "react";

const TOKEN_NAME = "access_token";

function useLocalStorage<T>(
  key: string,
  initialValue: T,
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(initialValue);

  useEffect(() => {
    try {
      const item = window.localStorage.getItem(key);
      if (item) {
        setStoredValue(JSON.parse(item));
      }
    } catch (error) {
      console.log(error);
    }
  }, [key]);

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.log(error);
    }
  };

  return [storedValue, setValue];
}

export const isLoggedIn: any = () => useLocalStorage(TOKEN_NAME, null);

export const removeAuthToken = (): void => {
  window.localStorage.removeItem(TOKEN_NAME);
};

export const setAuthToken = (token: string): void => {
  window.localStorage.setItem(TOKEN_NAME, token);
};
