import { useEffect, useState } from "react"
import { getAuth, subscribe, AuthSnapshot } from "@/utils/authState"

export function useAuthState(): AuthSnapshot {
  const [auth, setAuth] = useState<AuthSnapshot>(getAuth())

  useEffect(() => {
    return subscribe(() => setAuth(getAuth()))
  }, [])

  return auth
}
