import "@testing-library/jest-dom"
import "./helpers/api/mocks/server.setup"
import Storage from "dom-storage"
import fetch from "node-fetch"
import ResizeObserver from "resize-observer-polyfill"
import preloadAll from "jest-next-dynamic"

global.sessionStorage = new Storage(null, { strict: true })
/** In-memory localStorage, reset for each test file */
global.localStorage = new Storage(null, { strict: true })
/** Not an exact drop-in but hopefully good enough. Can be replaced with msw */
global.fetch = fetch as any
global.ResizeObserver = ResizeObserver

jest.mock("next/dist/client/router", () => require("next-router-mock"))

// Loads dynamic components so they are rendered.
beforeAll(() => preloadAll())
