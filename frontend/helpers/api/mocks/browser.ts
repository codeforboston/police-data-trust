import { setupWorker } from "msw"
import { handlers, rejectUnhandledApiRequests } from "./handlers"

export const worker = setupWorker(...handlers)

/** Starts worker, convenience for conditional importer */
export const startWorker = () => {
  worker.start({
    onUnhandledRequest: rejectUnhandledApiRequests
  })
}
