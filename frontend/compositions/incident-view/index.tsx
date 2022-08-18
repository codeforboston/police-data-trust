import IncidentViewHeader from "./incident-view-header"
import IncidentBody from "./incident-view-body"
import type { Incident } from "../../helpers/api"

export default function IncidentView(incident: Incident) {
  return (
    <>
      <IncidentViewHeader {...incident} />
      <IncidentBody {...incident} />
    </>
  )
}
