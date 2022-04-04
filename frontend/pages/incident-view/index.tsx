import { DashboardHeader } from "../../compositions"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import IncidentView from "../../compositions/incident-view"
import sampleIncident from "../../helpers/incident"

export default requireAuth(function () {
  const incident = sampleIncident()

  return (
    <Layout>
      <DashboardHeader />
      <IncidentView {...incident} />
    </Layout>
  )
})
