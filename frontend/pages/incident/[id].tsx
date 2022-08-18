import { requireAuth, useAuth } from "../../helpers"
import IncidentView from "../../compositions/incident-view"
import { useRouter } from "next/router"
import type { Incident } from "../../helpers/api"
import { useState } from "@storybook/addons"
import { useEffect } from "react"
import { getIncidentById } from "../../helpers/api"

export default requireAuth(function () {
  const [incident, setIncident] = useState<Incident>(undefined)
  const router = useRouter()
  const id = parseInt(String(router.query.id))
  const { accessToken } = useAuth()

  useEffect(() => {
    const getIncident = async () => {
      setIncident(await getIncidentById(id, accessToken))
    }

    getIncident()
  }, [id, accessToken])

  return isNaN(id) ? <p>Loading...</p> : <IncidentView {...incident} />
})
