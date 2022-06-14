import * as rtl from "@testing-library/react"
import { Providers } from "../helpers"
import { v4 as uuidv4 } from "uuid"
import * as htl from "@testing-library/react-hooks"
import router from "next/router"

// re-export testing libraries
export * from "@testing-library/react"
export * as hooks from "@testing-library/react-hooks"
export { default as userEvent } from "@testing-library/user-event"
export { default as router } from "next/router"
export { setAuthForTest } from "../helpers/auth"
export { server, rest } from "../helpers/api/mocks/server"

/** Renders components with application providers. */
export const render = (el: any, options?: any) => rtl.render(<Providers>{el}</Providers>, options)

/** Renders hooks with application providers. */
export const renderHook: typeof htl.renderHook = (callback, options) =>
  htl.renderHook(callback, { wrapper: Providers, ...options })

/** Returns an email for test that is likely to be unused. */
export const uniqueEmail = () => `${uuidv4()}@example.com`

/**
 * Pause for the given number of seconds. This is useful for debugging but
 * should never be used in a test to wait for something to happen. Use waitFor
 * or findBy queries instead.
 */
export const pause = (seconds: number) =>
  new Promise((r) => setTimeout(r, Math.round(seconds * 1000)))

export function setRouterForTest(path: string, query = {}) {
  router.pathname = path
  router.query = query
}
export function clearRouterForTest() {
  router.pathname = ""
  router.query = {}
}
