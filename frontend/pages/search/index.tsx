import * as React from "react"

import { DataTable } from "../../shared-components/data-table/data-table"
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout } from "../../shared-components"

export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
      <DataTable />
    </Layout>
  )
}
