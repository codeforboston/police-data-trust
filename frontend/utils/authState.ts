export type AuthSnapshot = {
  accessToken: string | null
  refreshAccessToken: () => Promise<string | null>
  readonly isLoggedIn: boolean
  logout?: () => void
}

let snapshot: Omit<AuthSnapshot, "isLoggedIn"> = {
  accessToken: null,
  refreshAccessToken: async () => null
}

type Listener = () => void
let listeners: Listener[] = []

export function setAuthRefresh(next: Omit<AuthSnapshot, "isLoggedIn">) {
  snapshot = next
  listeners.forEach((listener) => listener())
}

export function getAuth(): AuthSnapshot {
  return {
    ...snapshot,
    isLoggedIn: !!snapshot.accessToken
  }
}

export function subscribe(listener: Listener) {
  listeners.push(listener)
  return () => {
    listeners = listeners.filter((l) => l !== listener)
  }
}

// (optional, handy for tests)
export function resetAuth() {
  snapshot = { accessToken: null, refreshAccessToken: async () => null }
}
