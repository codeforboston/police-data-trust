// User Profile models
import { User } from "../helpers/api"

export enum ProfileMenu {
  USER_INFO = "info",
  PROFILE_TYPE = "type",
  SAVED_SEARCHES = "searches",
  SAVED_RESULTS = "results",
  NOTIFICATIONS = "notifications",
  ORGANIZATIONS = "organizations"
}

interface MenuText {
  item: ProfileMenu
  text: string
}

export const profileMenuItems: MenuText[] = [
  { item: ProfileMenu.USER_INFO, text: "User Information" },
  { item: ProfileMenu.PROFILE_TYPE, text: "Profile Type" },
  { item: ProfileMenu.SAVED_RESULTS, text: "Saved Results" },
  { item: ProfileMenu.SAVED_SEARCHES, text: "Saved Searches" },
  { item: ProfileMenu.NOTIFICATIONS, text: "Notifications" },
  { item: ProfileMenu.ORGANIZATIONS, text: "My Organizations" }
]

// props for profile menu content
export interface UserProfileProps {
  userData: UserDataType
}

/**
 * from backend/database/models/user.py
 */
export enum UserRoles {
  NONE = 0,
  PASSPORT = 1,
  PUBLIC = 2,
  CONTRIBUTOR = 3,
  ADMIN = 4
}

// User Information
export interface UserDataType {
  active: boolean
  firstName: string
  lastName: string
  email: string
  phone: string
  role: UserRoles
}

export const emptyUser: UserDataType = {
  active: false,
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  role: 0
}

export const publicUser = (user: User): UserDataType => ({
  firstName: user.firstName || "",
  lastName: user.lastName || "",
  email: user.email,
  phone: user.phoneNumber,
  active: user.active,
  role: UserRoles.PUBLIC
})

export const passportUser = (user: User): UserDataType => ({
  firstName: user.firstName || "",
  lastName: user.lastName || "",
  email: user.email,
  phone: user.phoneNumber,
  active: user.active,
  role: UserRoles.PASSPORT
})

export const contributorUser = (user: User): UserDataType => ({
  firstName: user.firstName || "",
  lastName: user.lastName || "",
  email: user.email,
  phone: user.phoneNumber,
  active: user.active,
  role: UserRoles.CONTRIBUTOR
})

export const adminUser = (user: User): UserDataType => ({
  firstName: user.firstName || "",
  lastName: user.lastName || "",
  email: user.email,
  phone: user.phoneNumber,
  active: user.active,
  role: UserRoles.ADMIN
})

export const someUser = (user: User, role: UserRoles): UserDataType => ({
  firstName: user.firstName || "",
  lastName: user.lastName || "",
  email: user.email,
  phone: user.phoneNumber,
  active: user.active,
  role: role
})

// Account Type
interface ProfileTypeText {
  title: string
  content: string
  linkText?: string
  linkPath?: string
}

export const profileTypeContent: { [key in UserRoles]: ProfileTypeText } = {
  [UserRoles.NONE]: {
    title: "No Account",
    content: "",
    linkText: "Sign up for an account",
    linkPath: "/register"
  },
  [UserRoles.PUBLIC]: {
    title: "Viewer Account",
    content:
      "A Viewer account allows you to see data that is publicly available. To apply to see legally protected data...",
    linkText: "Register for a Passport Account",
    linkPath: "/passport"
  },
  [UserRoles.PASSPORT]: {
    title: "Passport Account",
    content:
      "A Passport account allows you to see legally protected data. If the publicly available data is sufficient for your needs...",
    linkText: "Revert to a Viewer Account",
    linkPath: "/register"
  },
  [UserRoles.CONTRIBUTOR]: {
    title: "Contributor Account",
    content: ""
  },
  [UserRoles.ADMIN]: {
    title: "Administrator Account",
    content: ""
  }
}
