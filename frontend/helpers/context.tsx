import React, { ComponentProps, FC } from "react"
import { AuthProvider } from "."
import { FormProvider, useForm, useFormContext } from "react-hook-form"


export const combineComponents = (...components: FC[]): FC => {
  return components.reduce(
    (AccumulatedComponents, CurrentComponent) => {
      if (CurrentComponent === FormProvider) {
        const methods = useForm()
        CurrentComponent.apply(methods)
      }
      // eslint-disable-next-line react/display-name
      return ({ children }: ComponentProps<FC>): JSX.Element => {
        return (
          <AccumulatedComponents>
            <CurrentComponent>{children}</CurrentComponent>
          </AccumulatedComponents>
        )
      }
    },
    ({ children }) => <>{children}</>,
  )
}

const providers = [
  AuthProvider,
  FormProvider
]

export const contextProvider = combineComponents(...providers)