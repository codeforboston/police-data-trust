import * as React from 'react';

import { DataTable } from "../../shared-components/data-table/data-table"
import DashboardHeader from "../../compositions/dashboardHeader/index"
import Layout from '../../shared-components/layout/layout'

export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <DataTable />
    </Layout>
  )
}
