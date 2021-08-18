<<<<<<< HEAD
import * as React from 'react';

import { DataTable } from "../../shared-components/data-table/data-table"
import DashboardHeader from "../../compositions/dashboardHeader/index"
import Layout from '../../shared-components/layout/layout'
=======
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"
import { Layout } from "../../shared-components"
>>>>>>> 6dc649486a66f449ebc50b63b8d83b5b9a8fae57

export default function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
<<<<<<< HEAD
      <DataTable />
=======
      <Map />
>>>>>>> 6dc649486a66f449ebc50b63b8d83b5b9a8fae57
    </Layout>
  )
}
