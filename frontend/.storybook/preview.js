import { RouterContext } from "next/dist/shared/lib/router-context"

if (process.env.NODE_ENV === "development") {
  const { worker } = require("../helpers/api/mocks/browser")
  worker.start()
}

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/
    }
  },
  nextRouter: {
    Provider: RouterContext.Provider
  }
}
