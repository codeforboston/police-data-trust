import { DashboardHeader, Map, SearchResultsTable } from "../../compositions"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { InputForm, ResultsTable } from "../../compositions/basic-search"
import { SearchPanel } from "../../compositions/search/search-panel"
import PopUp from "../../compositions/visualizations/popUps/popUpComp"
import { usePopUp } from "../../compositions/visualizations/popUps/popUps"

type ChartType = "bubble" | "map"

export default requireAuth(function Dashboard() {
  return (
    <Layout>
      <div style={{ display: "flex" }}>
        <SearchPanel />
        <Map />
      </div>
      <InputForm />
      <SearchResultsTable />
      <ResultsTable />
    </Layout>
  )
})
