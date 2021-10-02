import { RouterContext } from "next/dist/shared/lib/router-context"
import { Providers } from "../helpers"
import { addDecorator } from "@storybook/react"
import { initialize, mswDecorator } from "msw-storybook-addon"

initialize()
addDecorator(mswDecorator)

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/
    }
  },
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ],
  nextRouter: {
    Provider: RouterContext.Provider
  }
}
