import { DashboardHeader, Map, SearchPanel, SearchResultsTable } from "../../compositions"
import { requireAuth, useSearch } from "../../helpers"
import { Layout } from "../../shared-components"
import styles from "./search.module.css"

export default requireAuth(function Dashboard() {
  const { searchPageContainer, searchPageDisplay } = styles
  const { incidentResults } = useSearch()

  return (
    <Layout>
      <div className={searchPageContainer}>
        <SearchPanel />
        <div className={searchPageDisplay}>
          <Map />
          {!!incidentResults && <SearchResultsTable />}
        </div>
      </div>
    </Layout>
  )
})
