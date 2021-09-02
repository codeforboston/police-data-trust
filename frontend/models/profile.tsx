
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


export const menuContent: { [key in ProfileMenu]: MenuText } = {
  [ProfileMenu.USER_INFO]: { item: ProfileMenu.USER_INFO, text: "User Information" },
  [ProfileMenu.PROFILE_TYPE]: { item: ProfileMenu.PROFILE_TYPE, text: "Profile Type" },
  [ProfileMenu.SAVED_RESULTS]: { item: ProfileMenu.SAVED_RESULTS, text: "Saved Results" },
  [ProfileMenu.SAVED_SEARCHES]: { item: ProfileMenu.SAVED_SEARCHES, text: "Saved Searches" }
}
