import { DashboardHeader } from "../../compositions"
import { OfficerHeader, OptionalOfficerInfo, OfficerWorkHistory, OfficerAffiliations } from "../../compositions/officer-view"
import { DataTable } from "../../shared-components/data-table/data-table"
import { resultsColumns } from "../../compositions/search-results/search-results"
import { EXISTING_TEST_INCIDENTS } from "../../helpers/api/mocks/data"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"

export default requireAuth(function OfficerView() {
  const timothy = getOfficerFromMockData(0)

  const tableProps = {
    tableName: "Involved Incidents",
    columns: resultsColumns,
    data: EXISTING_TEST_INCIDENTS
  }

  return (
    <Layout>
      <DashboardHeader />
      <OfficerHeader {...timothy} />
      <hr />
      <OptionalOfficerInfo {...timothy} />
      <hr />
      <OfficerWorkHistory {...timothy} />
      <OfficerAffiliations {...timothy} />
      <DataTable {...tableProps}/>
    </Layout>
  )
})
