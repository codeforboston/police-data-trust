import type { Metadata } from "next"
import "./globals.css"
import Nav from "@/components/Nav/nav"
import { inter, roboto } from "@/app/font"
import MobileNav from "../components/mobile_nav/mobileNav"
import { AuthProvider } from "@/providers/AuthProvider"
import { SearchProvider } from "@/providers/SearchProvider"
import { Suspense } from "react"
import { ThemeProvider } from "@mui/material/styles"
import theme from "@/utils/theme"

export const metadata: Metadata = {
  title: "NPDC (National Police Data Coalition)",
  description: "Is a national index of police incidents."
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <ThemeProvider theme={theme}>
        <Suspense
          fallback={
            <body>
              <div>Loading...</div>
            </body>
          }>
          <AuthProvider>
            <SearchProvider>
              <body className={`${inter.variable} ${roboto}`}>
                <Nav />
                <main>{children}</main>
                <MobileNav />
              </body>
            </SearchProvider>
          </AuthProvider>
        </Suspense>
      </ThemeProvider>
    </html>
  )
}
