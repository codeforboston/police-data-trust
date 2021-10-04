import { RouterContext } from "next/dist/shared/lib/router-context"
import { Providers } from "../helpers"
import { FormProvider, useForm } from "react-hook-form"
import { startWorker, worker } from "../helpers/api/mocks/browser"
import { setAuthForTest } from "../helpers/auth"

startWorker()

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

/**
 * Careful: decorators are applied from right to left
 */
export const decorators = [ProvideContexts, ConfigureMockServiceWorker, SetUser, ClearStorage]

/**
 * Wraps stories in contexts used by many components. This includes
 * application-global providers from the Providers component as well as
 * providers set up by specific components, such as FormProvider.
 */
function ProvideContexts(Story) {
  return (
    <Providers>
      <FormProvider {...useForm()}>
        <Story />
      </FormProvider>
    </Providers>
  )
}

/**
 * Applies default mock handlers to the service worker and any additional
 * handlers specified in `Story.parameters.msw`.
 *
 * Lifted from https://github.com/mswjs/msw-storybook-addon/blob/master/packages/msw-addon/src/mswDecorator.js#L39
 */
function ConfigureMockServiceWorker(Story, { parameters: { msw = [] } }) {
  // Resets to default handlers
  worker.resetHandlers()

  if (!Array.isArray(msw)) {
    throw new Error(`[MSW] expected to receive an array of handlers but received "${typeof msw}" instead.
      Please refer to the documentation: https://mswjs.io/docs/getting-started/mocks/`)
  }

  if (msw.length > 0) {
    worker.use(...msw)
  }

  return <Story />
}

/** Set the cached user for testing. */
function SetUser(Story, { parameters: { user = true } }) {
  if (user) {
    if (typeof user === "boolean") {
      // use default user
      user = undefined
    }

    setAuthForTest(user)
  }
  return <Story />
}

/** Clear storage so each story starts from a consistent place. */
function ClearStorage(Story) {
  localStorage.clear()
  sessionStorage.clear()
  return <Story />
}
