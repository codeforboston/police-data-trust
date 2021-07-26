import DashboardHeader from "../../compositions/dashboardHeader/index"
import Map from "../../compositions/map"
import styles from "../../compositions/dashboardHeader/header.module.css"
import Layout from "../../shared-components/layout/Layout"


export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
    </Layout>
  )
}
