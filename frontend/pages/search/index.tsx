import { DataTable } from "../../shared-components/data-table/data-table"
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout } from "../../shared-components"
import { requireAuth } from "../../helpers"

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
      <DataTable />
    </Layout>
  )
})
