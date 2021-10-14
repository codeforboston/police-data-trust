import { setupServer } from "msw/node"
import { handlers } from "./handlers"

export { rest } from "msw"
export const server = setupServer(...handlers)
