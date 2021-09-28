import { useEffect } from "react"

let apiMode = process.env.NEXT_PUBLIC_API_MODE
if (!apiMode) {
  apiMode = process.env.NODE_ENV === "development" ? "mock" : "real"
}

export function useMockServiceWorker() {
  useEffect(() => {
    if (apiMode === "mock") {
      import("./browser").then(({ startWorker }) => startWorker())
    }
  }, [])
}
