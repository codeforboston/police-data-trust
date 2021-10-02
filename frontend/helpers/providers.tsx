import { AuthProvider } from "./auth"
import { FormProvider, useForm } from "react-hook-form"

/**
 * Wraps components in application providers, which set up contexts to provide
 * services to components.
 */
export const Providers: React.FC = ({ children }) => (
  <AuthProvider>
    <FormProvider {...useForm()}>
      {children}
    </FormProvider>
  </AuthProvider>
)
