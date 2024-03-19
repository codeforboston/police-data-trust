import { GetServerSidePropsContext, InferGetServerSidePropsType } from "next"
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
import { useProfileTab } from "./useProfileTab"

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { query } = context
  const initialTab: ProfileMenu = Object.values(ProfileMenu).includes(query.tab as ProfileMenu)
    ? (query.tab as ProfileMenu)
    : ProfileMenu.USER_INFO

  if (initialTab !== query.tab) {
    // An invalid tab was requested,
    // Redirect to ProfileMenu.USER_INFO tab
    return {
      redirect: {
        destination: `/profile?tab=${initialTab}`,
        permanent: false
      }
    }
  }

  return {
    props: {
      initialTab
    }
  }
}

export default requireAuth(function Profile({
  initialTab
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const [activePage, handleTabChange] = useProfileTab(initialTab)

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
        return ProfileOrganizations
      default:
        throw new Error("Must be a key in 'ProfileMenu' enum - unexpected default case!")
    }
  })(activePage)

  return (
    <Layout>
      <div className={styles.profileWrapper}>
        <ProfileNav activePage={activePage} setActivePage={handleTabChange} />
        <ActivePageComp />
      </div>
    </Layout>
  )
})
