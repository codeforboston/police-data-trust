import IncidentViewHeader from "./incident-view-header"
import IncidentBody from "./incident-view-body"
import { Incident } from "../../helpers/incident"

export default function IncidentView(incident: Incident) {
  return (
    <>
      <IncidentViewHeader {...incident} />
      <IncidentBody {...incident} />
    </>
  )
}
