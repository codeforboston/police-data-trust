import { useAuth } from "../../helpers"
import { renderHook, setAuthForTest } from "../test-utils"

beforeEach(() => localStorage.clear())

it("Sets auth data for tests", () => {
  setAuthForTest()

  const {
    result: {
      current: { user, accessToken }
    }
  } = renderHook(() => useAuth())

  expect(user.email).toBeTruthy()
  expect(accessToken).toBeTruthy()
})
