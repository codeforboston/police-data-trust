import * as React from "react"

import { Layout } from "../../shared-components"
import { DashboardHeader } from "../../compositions"
import ProfileNav from "../../compositions/profile-nav/profile-nav"
import { ProfileMenu } from "../../models/profile"
import {
  ProfileInfo,
  ProfileType,
  SavedSearches,
  SavedResults
} from "../../compositions/profile-content"
import styles from "./profile.module.css"

// TODO: replace with API call
import {users} from "../../models/mock-data"

export default function Profile() {
  const [nav, setNav] = React.useState(ProfileMenu.USER_INFO)

  const mockUser = users[0]

  return (
    <Layout>
      <DashboardHeader />
      <div className={styles.profileWrapper}>
        <ProfileNav currentItem={nav} selectNav={setNav} />

        {nav === ProfileMenu.USER_INFO && <ProfileInfo userData={mockUser} />}
        {nav === ProfileMenu.PROFILE_TYPE && <ProfileType userData={mockUser} />}
        {nav === ProfileMenu.SAVED_SEARCHES && <SavedSearches userData={mockUser} />}
        {nav === ProfileMenu.SAVED_RESULTS && <SavedResults userData={mockUser} />}
      </div>
    </Layout>
  )
}
