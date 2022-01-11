import React from "react"
import { Layout } from "../../shared-components"
import { Logo as NPDCLogo } from "../../shared-components"
import styles from "../../compositions/dashboard-header/dashboard-header.module.css"

import { LogoSizes } from "../../models"
import { requireAuth, useAuth } from "../../helpers"

export default requireAuth(function Logout() {
  const { leftHeader, titleContainer, mobileTitle, desktopTitle } = styles
  const { logout } = useAuth()
  React.useEffect(() => {
    logout()
  }, [logout])
  return (
    <Layout>
      <section className="enrollmentSection">
        <div className={leftHeader}>
          <NPDCLogo size={LogoSizes.MEDIUM} />
          <div className={titleContainer}>
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>
      </section>
    </Layout>
  )
})
