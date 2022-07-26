import { requireAuth } from "../../helpers"
import IncidentView from "../../compositions/incident-view"
import getIncident from "../../helpers/incident"
import { useRouter } from "next/router"

export default requireAuth(function () {
  const router = useRouter()
  try {
    const id = parseInt(String(router.query.id))
    const incident = getIncident(id)
    return <IncidentView {...incident} />
  } catch (e) {
    return null
  }
})
