import { RouterContext } from "next/dist/shared/lib/router-context"
// import { addDecorator } from "@storybook/react"
// import { withContexts } from "@storybook/addon-contexts/react"
// import { contexts } from "./contexts"

// addDecorator(withContexts(contexts))

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
