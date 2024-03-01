import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { Toaster } from "react-hot-toast"
import { AuthProvider } from "./auth"
import { SearchProvider } from "./search"

/**
 * Query Client responsible for housing cache of
 * network requests, serves as basis
 * for React Query functionality
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
      retry: false
    }
  }
})

/**
 * Wraps components in application providers, which set up contexts to provide
 * services to components.
 */
export const Providers: React.FC = ({ children }) => (
  <>
    <QueryClientProvider client={queryClient}>
      <ReactQueryDevtools />
      <Toaster position="bottom-right" />
      <AuthProvider>
        <SearchProvider>{children}</SearchProvider>
      </AuthProvider>
    </QueryClientProvider>
  </>
)
