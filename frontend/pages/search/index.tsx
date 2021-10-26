import { useState } from "react"
import { DashboardHeader, Map } from "../../compositions"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { InputForm, ResultsTable } from "../../compositions/basic-search"
import { DataTable } from "../../shared-components/data-table/data-table"

type ChartType = "bubble" | "map"

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
      <InputForm />
      <ResultsTable />
    </Layout>
  )
})
