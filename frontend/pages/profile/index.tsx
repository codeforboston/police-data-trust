import * as React from "react"

import { Layout } from "../../shared-components"
import { DashboardHeader } from "../../compositions"
import ProfileNav from "../../compositions/profile-nav/profile-nav"
import { ProfileMenu } from "../../models/profile"

export default function Profile() {
  const [nav, setNav] = React.useState(ProfileMenu.USER_INFO)
  return (
    <Layout>
      <DashboardHeader />
      <ProfileNav currentItem={nav} selectNav={setNav} />
      <div>placeholder</div>
    </Layout>
  )
}
