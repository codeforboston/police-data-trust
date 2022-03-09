import * as React from "react"
import { Layout } from "../../shared-components"
import { ProfileMenu } from "../../models/profile"
import { requireAuth } from "../../helpers"
import {
  DashboardHeader,
  ProfileInfo,
  ProfileNav,
  ProfileType,
  SavedSearches,
  SavedResults
} from "../../compositions"
import styles from "./profile.module.css"
// import { useAuth, requireAuth } from "../../helpers"

export default requireAuth(function Profile() {
  const [nav, setNav] = React.useState(ProfileMenu.USER_INFO)

  return (
    <Layout>
      <div className={styles.profileWrapper}>
        <ProfileNav currentItem={nav} selectNav={setNav} />

        {/* TODO: this looks awful */}
        {nav === ProfileMenu.USER_INFO && <ProfileInfo />}
        {nav === ProfileMenu.PROFILE_TYPE && <ProfileType />}
        {nav === ProfileMenu.SAVED_RESULTS && <SavedResults />}
        {nav === ProfileMenu.SAVED_SEARCHES && <SavedSearches />}
      </div>
    </Layout>
  )
})
