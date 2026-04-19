const API_ROUTES = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
    refresh: "/auth/refresh",
    forgotPassword: "/auth/forgotPassword",
    whoami: "/auth/whoami"
  },
  search: {
    all: "/search",
    incidents: "/incidents/search",
    officers: "/officers",
    agencies: "/agencies",
    units: "/units",
    complaints: "/complaints"
  },
  users: {
    self: "/users/self",
    profile: (uid: string) => `/users/${uid}`,
    peopleSuggestions: "/users/self/suggestions/people"
  },
  sources: {
    all: "/sources",
    profile: (identifier: string) => `/sources/${identifier}`,
    profileBySlug: (slug: string) => `/sources/slug/${slug}`,
    members: (uid: string) => `/sources/${uid}/members`,
    activity: (uid: string) => `/sources/${uid}/activity`
  },
  officers: {
    profile: (slug: string) => `/officers/${slug}`
  },
  agencies: {
    all: "/agencies",
    relevant: "/agencies/relevant",
    profile: (slug: string) => `/agencies/${slug}`
  },
  units: {
    profile: (slug: string) => `/units/${slug}`
  }
}

export const apiBaseUrl: string =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5001/api/v1"

export default API_ROUTES
