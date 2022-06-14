import { requireAuth } from "../../helpers"
import IncidentView from "../../compositions/incident-view"
import sampleIncident from "../../helpers/incident"

export default requireAuth(function () {
  const incident = sampleIncident()

  return <IncidentView {...incident} />
})
