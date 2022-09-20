import { requireAuth, useAuth } from "../../helpers"
import IncidentView from "../../compositions/incident-view"
import { useRouter } from "next/router"
import type { Incident } from "../../helpers/api"
import { useEffect, useState } from "react"
import { getIncidentById } from "../../helpers/api"

export default requireAuth(function IncidentDetailsView() {
  const [incident, setIncident] = useState<Incident>(undefined)
  const router = useRouter()
  const id = parseInt(String(router.query.id))
  const { accessToken } = useAuth()

  useEffect(() => {
    if (isNaN(id)) return
    getIncidentById(id, accessToken).then((i) => setIncident(i))
  }, [id, accessToken])

  return incident ? <IncidentView {...incident} /> : <p>Loading...</p>
})
