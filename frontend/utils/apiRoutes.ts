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
    incidents: "/incidents/search",
    officers: "/officers"
  },
  users: {
    self: "/users/self"
  },
  sources: {
    all: "/sources/"
  }
}

export const apiBaseUrl: string =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5001/api/v1"

export default API_ROUTES
