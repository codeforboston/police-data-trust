import { RouterContext } from "next/dist/shared/lib/router-context"
// import { addDecorator } from "@storybook/react"
// import { withContexts } from "@storybook/addon-contexts/react"
// import { contexts } from "./contexts"
import { worker } from "../helpers/api/mocks/browser"
import FakeAuth from "../helpers/api/mocks/fake-auth"

// addDecorator(withContexts(contexts))

if (typeof global.process === "undefined") {
  worker.start()
  // FakeAuth.start()
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
