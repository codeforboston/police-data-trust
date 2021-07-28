import DashboardHeader from "../../compositions/dashboardHeader/index"
import styles from "../../compositions/dashboardHeader/header.module.css"

import Layout from "../../shared-components/layout/Layout"

export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
    </Layout>
  )
}
