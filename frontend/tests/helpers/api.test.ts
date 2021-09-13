import jwt, { JwtPayload } from "jsonwebtoken"
import { login, register, whoami } from "../../helpers"
import { AccessToken, NewUser } from "../../helpers/api"
import { uniqueEmail } from "../test-utils"

/** Must match alembic/dev_seeds.py */
const EXISTING_TEST_USER = { email: "test@example.com", password: "password" }

/** Must match backend/config.py  */
const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY || "my-jwt-secret-key"

describe("api", () => {
  describe("login", () => {
    it("authenticates", async () => {
      const token = await login(EXISTING_TEST_USER)
      expect(token).toBeTruthy()
    })
  })

  describe("whoami", () => {
    it("retrieves the authenticated user", async () => {
      const accessToken = await login(EXISTING_TEST_USER)
      const user = await whoami({ accessToken })
      expect(user).toEqual({
        active: true,
        email: "test@example.com",
        emailConfirmedAt: null,
        firstName: "Test",
        lastName: "Example"
      })
    })

    it("fails if token is expired", async () => {
      let accessToken = await login(EXISTING_TEST_USER)
      accessToken = updateToken(accessToken, { exp: 0 })

      const error = await whoami({ accessToken }).catch((e) => e)
      expect(error.response.status).toEqual(401)
    })

    it("fails if not authenticated", async () => {
      let error = await whoami({ accessToken: undefined }).catch((e) => e)
      expect(error.response.status).toEqual(401)

      error = await whoami({ accessToken: "badtoken" }).catch((e) => e)
      expect(error.response.status).toEqual(422)
    })
  })

  describe("register", () => {
    it("registers new users", async () => {
      const newUser: NewUser = {
        email: uniqueEmail(),
        password: "password",
        firstName: "June",
        lastName: "Grey"
      }

      const accessToken = await register(newUser)
      expect(accessToken).toBeTruthy()
      const user = await whoami({ accessToken })

      expect(user.email).toEqual(newUser.email)
      expect(user.firstName).toEqual(newUser.firstName)
      expect(user.lastName).toEqual(newUser.lastName)
    })
  })
})

/** Modifies the payload of a JWT token. */
function updateToken(
  accessToken: AccessToken,
  update: Partial<JwtPayload>,
  secret: string = JWT_SECRET_KEY
): AccessToken {
  const payload = jwt.verify(accessToken, secret) as JwtPayload
  return jwt.sign({ ...payload, ...update }, secret)
}
