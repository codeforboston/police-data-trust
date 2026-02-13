const API_ROUTES = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
    refresh: "/auth/refresh",
    forgotPassword: "/auth/forgotPassword",
    whoami: "/auth/whoami"
  },
  search: {
    all: "/search/",
    incidents: "/incidents/search"
  },
  users: {
    self: "/users/self"
  },
  sources: {
    all: "/sources/"
  },
  officers: {
    profile: (slug: string) => `/officers/${slug}`
  }
}

export const apiBaseUrl: string =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5001/api/v1"

export default API_ROUTES
