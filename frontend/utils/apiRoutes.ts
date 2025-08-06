const API_ROUTES = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
    forgotPassword: "/auth/forgotPassword"
  },
  search: {
    all: "/search/",
    incidents: "/incidents/search"
  }
}

export const apiBaseUrl: string =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5001/api/v1"

export default API_ROUTES
