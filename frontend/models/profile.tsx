// User Profile models

export enum ProfileMenu {
  USER_INFO = 'info',
  PROFILE_TYPE = 'type',
  SAVED_SEARCHES = 'searches',
  SAVED_RESULTS = 'results'
}

interface MenuText {
  item: ProfileMenu,
  text: string
}


export const menuContent: {
  [key in ProfileMenu]: MenuText
} = {
  [ProfileMenu.USER_INFO]: {
    item: ProfileMenu.USER_INFO,
    text: "User Information"
  },
  [ProfileMenu.PROFILE_TYPE]: {
    item: ProfileMenu.PROFILE_TYPE,
    text: "Profile Type"
  },
  [ProfileMenu.SAVED_RESULTS]: {
    item: ProfileMenu.SAVED_RESULTS,
    text: "Saved Results"
  },
  [ProfileMenu.SAVED_SEARCHES]: {
    item: ProfileMenu.SAVED_SEARCHES,
    text: "Saved Searches"
  }
}


// props for profile menu content
export interface UserProfileProps {
  userData: UserType
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
  role: 0
}


// Account Type
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