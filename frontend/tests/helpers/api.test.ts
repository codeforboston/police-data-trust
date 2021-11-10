import { api } from "../../helpers"
import { EXISTING_TEST_INCIDENTS, EXISTING_TEST_USER } from "../../helpers/api/mocks/data"
import { uniqueEmail } from "../test-utils"

describe("api", () => {
  describe("login", () => {
    it("authenticates", async () => {
      const token = await api.login(EXISTING_TEST_USER)
      expect(token).toBeTruthy()
    })

    it("fails if incorrect login", async () => {
      const e = await api
        .login({ email: EXISTING_TEST_USER.email, password: "wrong" })
        .catch((e) => e)
      expect(e.response.status).toEqual(401)
    })
  })

  describe("whoami", () => {
    it("retrieves the authenticated user", async () => {
      const accessToken = await api.login(EXISTING_TEST_USER)
      const user = await api.whoami({ accessToken })
      expect(user).toEqual({
        active: true,
        email: "test@example.com",
        emailConfirmedAt: null,
        firstName: "Test",
        lastName: "Example",
        phoneNumber: "(123) 456-7890",
        role: "Public"
      })
    })

    it("fails if not authenticated", async () => {
      let error = await api.whoami({ accessToken: undefined }).catch((e) => e)
      expect(error.response.status).toEqual(401)
    })
  })

  describe("register", () => {
    it("registers new users", async () => {
      const newUser: api.NewUser = {
        email: uniqueEmail(),
        password: "password",
        firstName: "June",
        lastName: "Grey",
        phoneNumber: "(555) 555-5555"
      }

      const accessToken = await api.register(newUser)
      expect(accessToken).toBeTruthy()
      const user = await api.whoami({ accessToken })

      expect(user.email).toEqual(newUser.email)
      expect(user.firstName).toEqual(newUser.firstName)
      expect(user.lastName).toEqual(newUser.lastName)
      expect(user.phoneNumber).toEqual(newUser.phoneNumber)
    })

    it("rejects existing accounts", async () => {
      const newUser: api.NewUser = {
        email: EXISTING_TEST_USER.email,
        password: "password",
        firstName: "June",
        lastName: "Grey"
      }

      let error = await api.register(newUser).catch((e) => e)
      expect(error.response.status).toBe(400)
    })
  })

  describe("searchIncidents", () => {
    it.each([
      [
        "Filters by date",
        {
          startTime: "09-01-2019",
          endTime: "10-15-2019",
          description: "Test description",
          location: "Test location"
        },
        [EXISTING_TEST_INCIDENTS[0]]
      ],
      [
        "Finds all test incidents",
        {
          description: "Test description",
          location: "Test location"
        },
        EXISTING_TEST_INCIDENTS
      ]
    ])("%s", async (title, query, expectedIncidents) => {
      const accessToken = await api.login(EXISTING_TEST_USER)

      const response = await api.searchIncidents({
        accessToken,
        ...query
      })

      expect(response.page).toBe(1)
      expect(response.totalPages).toBe(1)
      expect(response.totalResults).toBe(expectedIncidents.length)
      expect(response.results).toHaveLength(expectedIncidents.length)

      for (const actual of response.results) {
        const expected = expectedIncidents.find((i) => i.id === actual.id)
        expect(expected).toBeDefined()
        expect(actual).toMatchObject(expected)
      }
    })
  })
})
