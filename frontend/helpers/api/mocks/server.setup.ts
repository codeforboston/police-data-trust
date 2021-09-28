import { rejectUnhandledApiRequests } from "./handlers"
import { server } from "./server"

beforeAll(() =>
  server.listen({
    onUnhandledRequest: rejectUnhandledApiRequests
  })
)

afterEach(() => server.resetHandlers())

afterAll(() => server.close())
