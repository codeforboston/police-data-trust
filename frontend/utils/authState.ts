export type AuthSnapshot = {
  accessToken: string | null
  refreshAccessToken: () => Promise<string | null>
  logout?: () => void
}

let snapshot: AuthSnapshot = {
  accessToken: null,
  refreshAccessToken: async () => null,
}

export function setAuthRefresh(next: AuthSnapshot) {
  snapshot = next
}

export function getAuth(): AuthSnapshot {
  return snapshot
}

// (optional, handy for tests)
export function resetAuth() {
  snapshot = { accessToken: null, refreshAccessToken: async () => null }
}
