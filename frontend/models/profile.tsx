// User Profile models

import { SavedResults, SavedSearch } from "../compositions/profile-content"
import ProfileInfo from "../compositions/profile-content/profile-info"
import ProfileType from "../compositions/profile-content/profile-type"

export enum ProfileMenu {
  USER_INFO = 'info',
  PROFILE_TYPE = 'type',
  SAVED_SEARCHES = 'searches',
  SAVED_RESULTS = 'results'
}

interface MenuText {
  item: ProfileMenu,
  text: string,
  component: Function
}


export const menuContent: {
  [key in ProfileMenu]: MenuText
} = {
  [ProfileMenu.USER_INFO]: {
    item: ProfileMenu.USER_INFO,
    text: "User Information",
    component: ProfileInfo
  },
  [ProfileMenu.PROFILE_TYPE]: {
    item: ProfileMenu.PROFILE_TYPE,
    text: "Profile Type",
    component: ProfileType
  },
  [ProfileMenu.SAVED_RESULTS]: {
    item: ProfileMenu.SAVED_RESULTS,
    text: "Saved Results",
    component: SavedResults
  },
  [ProfileMenu.SAVED_SEARCHES]: {
    item: ProfileMenu.SAVED_SEARCHES,
    text: "Saved Searches",
    component: SavedSearch
  }
}

export interface UserProfileProps {
  userData: UserType
}


export enum UserRoles {
  NONE = 0,
  PASSPORT = 1,
  PUBLIC = 2,
  CONTRIBUTOR = 3,
  ADMIN = 4
}

export interface UserType {
  id: number,
  active: boolean,
  firstName: string,
  lastName: string,
  email: string,
  emailConfirmedAt?: Date,
  phone: string,
  pwHash: string,
  role: UserRoles
}

export const emptyUser: UserType = {
  id: 0,
  active: false,
  firstName: '',
  lastName: '',
  email: '',
  pwHash: '',
  phone: '',
  role: UserRoles.NONE
}


interface ProfileTypeText {
  title: string,
  content: string,
  linkText?: string,
  linkPath?: string
}

export const profileTypeContent: { [key in UserRoles]: ProfileTypeText} = {
  [UserRoles.NONE]: {
    title: 'No Account',
    content: '',
    linkText: 'Sign up for an account',
    linkPath: '/register'
  },
  [UserRoles.PUBLIC]: {
    title: 'Viewer Account',
    content: 'A Viewer account allows you to see data that is publicly available. To apply to see legally protected data...',
    linkText: 'Register for a Passport Account',
    linkPath: '/passport'
  },
  [UserRoles.PASSPORT]: {
    title: 'Passport Account',
    content: 'A Passport account allows you to see legally protected data. If the publicly available data is sufficient for your needs...',
    linkText: 'Revert to a Viewer Account',
    linkPath: '/register'
  },
  [UserRoles.CONTRIBUTOR]: {
    title: 'Contributor Account',
    content: ''
  },
  [UserRoles.ADMIN]: {
    title: 'Administrator Account',
    content: ''
  }
}