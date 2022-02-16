import { access } from "fs"
import { MockedRequest, rest } from "msw"
import { baseURL, IncidentSearchRequest, LoginCredentials, NewUser, ForgotPassword } from ".."
import FakeAuth from "./fake-auth"
import FakeSearch from "./fake-search"

type Json = Record<string, any>

const auth = new FakeAuth()
const search = new FakeSearch()

export const handlers = [
  rest.post<Json>(routePath("/auth/login"), (req, res, ctx) => {
    const token = auth.login(req.body as LoginCredentials)
    if (token) {
      return res(ctx.status(200), ctx.json({ access_token: token }))
    }
    return res(ctx.status(401))
  }),

  rest.post<Json>(routePath("/auth/register"), (req, res, ctx) => {
    const token = auth.register(req.body as NewUser)
    if (!token) {
      return res(ctx.status(400), ctx.json({ message: "email matches existing account" }))
    }
    return res(ctx.status(200), ctx.json({ access_token: token }))
  }),

  rest.post<Json>(routePath("/auth/forgotPassword"), (req, res, ctx) => {
    if (req.body.email) {
      return res(ctx.status(200))
    } else {
      return res(ctx.status(422))
    }
  }),

  rest.post<Json>(routePath("/auth/resetPassword"), (req, res, ctx) => {
    const accessToken = req.headers.get("Authorization")?.match(/^Bearer (?<token>.*)$/)
      ?.groups?.token
    const user = accessToken && auth.whoami(accessToken)

    if (!user) {
      return res(ctx.status(401))
    }

    const { password } = req.body
    try {
      const message = auth.reset({ accessToken, password })
      return res(ctx.json({ message }), ctx.status(200))
    } catch (e) {
      return res(
        ctx.status(401),
        ctx.json({
          message: e.message
        })
      )
    }
  }),

  rest.get(routePath("/auth/whoami"), (req, res, ctx) => {
    const token = req.headers.get("Authorization")?.match(/^Bearer (?<token>.*)$/)?.groups?.token
    const user = token && auth.whoami(token)

    if (!user) {
      return res(ctx.status(401))
    }

    return res(
      ctx.status(200),
      ctx.json({
        active: user.active,
        email: user.email,
        email_confirmed_at: user.emailConfirmedAt,
        first_name: user.firstName,
        last_name: user.lastName,
        phone_number: user.phoneNumber,
        role: user.role
      })
    )
  }),

  rest.post<Json>(routePath("/incidents/search"), (req, res, ctx) => {
    const query = req.body as IncidentSearchRequest
    return res(ctx.status(200), ctx.json(search.search(query)))
  })
]

/** Require that all API requests to our backend be handled. */
export function rejectUnhandledApiRequests(req: MockedRequest) {
  const url = req.url.href
  if (url.startsWith(baseURL)) {
    throw new Error("Unhandled API request in mock service worker handlers! " + url)
  }
}

/** Returns the absolute URL for the relative path */
export function routePath(relative: string) {
  return `${baseURL}${relative}`
}
