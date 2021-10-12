import { useEffect } from "react"

export const apiMode = (() => {
  const apiMode = process.env.NEXT_PUBLIC_API_MODE
  switch (apiMode) {
    case "real":
      return "real"
    case "mock":
      return "mock"
    case undefined:
      return process.env.NODE_ENV === "development" ? "mock" : "real"
    default:
      throw Error("Invalid api mode " + apiMode)
  }
})()

export function useMockServiceWorker() {
  useEffect(() => {
    if (apiMode === "mock") {
      import("./browser").then(({ startWorker }) => startWorker())
    }
  }, [])
}
