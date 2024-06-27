import { setupWorker } from "msw"
import { handlers, rejectUnhandledApiRequests } from "./handlers"

export const worker = setupWorker(...handlers)

/** Starts worker, convenience for conditional import */
export const startWorker = () => {
  worker.start({
    onUnhandledRequest: rejectUnhandledApiRequests
  })
}
