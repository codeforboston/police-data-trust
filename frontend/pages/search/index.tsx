import { DashboardHeader, Map, SearchResultsTable } from "../../compositions"
import { InputForm, ResultsTable } from "../../compositions/basic-search"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <DashboardHeader />
      <Map />
      <InputForm />
      <SearchResultsTable />
      <ResultsTable />
    </Layout>
  )
})
