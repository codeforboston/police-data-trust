import { login, register, whoami } from "../../helpers"
import { NewUser } from "../../helpers/api"
import { EXISTING_TEST_USER } from "../../helpers/api/mocks/data"
import { uniqueEmail } from "../test-utils"

describe("api", () => {
  describe("login", () => {
    it("authenticates", async () => {
      const token = await login(EXISTING_TEST_USER)
      expect(token).toBeTruthy()
    })

    it("fails if incorrect login", async () => {
      const e = await login({ email: EXISTING_TEST_USER.email, password: "wrong" }).catch((e) => e)
      expect(e.response.status).toEqual(401)
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

    it("fails if not authenticated", async () => {
      let error = await whoami({ accessToken: undefined }).catch((e) => e)
      expect(error.response.status).toEqual(401)
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

    it("rejects existing accounts", async () => {
      const newUser: NewUser = {
        email: EXISTING_TEST_USER.email,
        password: "password",
        firstName: "June",
        lastName: "Grey"
      }

      let error = await register(newUser).catch((e) => e)
      expect(error.response.status).toBe(400)
    })
  })
})
