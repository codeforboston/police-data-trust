import { requireAuth } from "../../helpers"
import IncidentView from "../../compositions/incident-view"
import getIncident from "../../helpers/incident"
import { useRouter } from "next/router"

export default requireAuth(function () {
  const router = useRouter()
  const id = parseInt(String(router.query.id))
  return isNaN(id) ? <p>Loading...</p> : <IncidentView {...getIncident(id)} />
})
