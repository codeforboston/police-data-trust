import React from "react"
import { DashboardHeader, Map } from "../../compositions"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { InputForm, ResultsTable } from "../../compositions/basic-search"
import { SearchPanel } from "./search-panel"

type ChartType = "bubble" | "map"

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <SearchPanel />
      <Map />
      <InputForm />
      <ResultsTable />
    </Layout>
  )
})
