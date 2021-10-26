import { server } from "../test-utils"

/** Turn off API mocking for the test so we use the real API */
beforeAll(() => server.close())

/** Re-import the main test file to pick up the tests */
require("./api.test")
