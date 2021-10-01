import { RouterContext } from "next/dist/shared/lib/router-context"
// import { FormProvider, useForm } from "react-hook-form"
// import { AuthProvider } from "../helpers"
// import { addDecorator } from "@storybook/react"
// import { initializeWorker, mswDecorator } from "msw-storybook-addon"

// initializeWorker()
// addDecorator(mswDecorator)

// don't run in production or during build
// if (process.env.NODE_ENV === "development" && typeof global.process === 'undefined') {
//   const { worker } = require("../helpers/api/mocks/browser")
//   worker.start()
// }

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/
    }
  },
  // decorators: [
  //   (Story) => {
  //     const methods = useForm()
  //     return (
  //       <AuthProvider>
  //         <FormProvider {...methods}>
  //           <Story />
  //         </FormProvider>
  //       </AuthProvider>
  //     )
  //   }
  // ],
  nextRouter: {
    Provider: RouterContext.Provider
  }
}
