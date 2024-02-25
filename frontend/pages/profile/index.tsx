import * as React from "react"
import {
  ProfileInfo,
  ProfileNav,
  ProfileNotifications,
  ProfileOrganizations,
  ProfileType,
  SavedResults,
  SavedSearches
} from "../../compositions"
import { requireAuth } from "../../helpers"
import { ProfileMenu } from "../../models/profile"
import { Layout } from "../../shared-components"
import styles from "./profile.module.css"
import OrgUserTable from "../../compositions/profile-orguser/profile-orguser"

export default requireAuth(function Profile() {
  const [activePage, setActivePage] = React.useState(ProfileMenu.USER_INFO)

  const ActivePageComp = (function (menuItem: ProfileMenu) {
    switch (menuItem) {
      case ProfileMenu.USER_INFO:
        return ProfileInfo
      case ProfileMenu.PROFILE_TYPE:
        return ProfileType
      case ProfileMenu.SAVED_RESULTS:
        return SavedResults
      case ProfileMenu.SAVED_SEARCHES:
        return SavedSearches
      case ProfileMenu.NOTIFICATIONS:
        return ProfileNotifications
      case ProfileMenu.ORGANIZATIONS:
        // return ProfileOrganizations
        return OrgUserTable
      default:
        throw new Error("Must be a key in 'ProfileMenu' enum - unexpected default case!")
    }
  })(activePage)

  return (
    <Layout>
      <div className={styles.profileWrapper}>
        <ProfileNav activePage={activePage} setActivePage={setActivePage} />
        <ActivePageComp />
      </div>
    </Layout>
  )
})
