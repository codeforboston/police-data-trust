import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout } from "../../shared-components"

export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
    </Layout>
  )
}
