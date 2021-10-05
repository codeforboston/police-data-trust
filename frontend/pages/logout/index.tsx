import React from "react"
import { Layout } from "../../shared-components"
import { Logo as NPDCLogo } from "../../shared-components"
import styles from "../../compositions/dashboard-header/dashboard-header.module.css"

import { LogoSizes } from "../../models"
import { useAuth } from "../../helpers"

export default function Logout() {
  const { leftHeader, mobileLogo, desktopLogo, titleContainer, mobileTitle, desktopTitle } = styles
  // const { logout } = useAuth()

  return (
    <Layout>
      <section className="enrollmentSection">
        <div className={leftHeader}>
          <div className={mobileLogo}>
            <NPDCLogo size={LogoSizes.SMALL} />
          </div>
          <div className={desktopLogo}>
            <NPDCLogo size={LogoSizes.MEDIUM} />
          </div>
          <div className={titleContainer}>
            <h2 className={mobileTitle}>N.P.D.C.</h2>
            <h2 className={desktopTitle}>National Police Data Coalition</h2>
            <p>The national index of police incidents</p>
          </div>
        </div>
      </section>
    </Layout>
  )
}
