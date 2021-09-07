import { AppRoutes } from "."

export interface NavTypes {
  loc: AppRoutes
  text: string
}

export const headerTabs: NavTypes[] = [
  { loc: AppRoutes.DASHBOARD, text: "Search" },
  { loc: AppRoutes.PROFILE, text: "Profile" },
  { loc: AppRoutes.ABOUT, text: "About" }
]
