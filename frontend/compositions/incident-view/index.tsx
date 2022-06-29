import IncidentViewHeader from "./incident-view-header"
import IncidentBody from "./incident-view-body"
import type { IncidentRecordType } from "../../models"

export default function IncidentView(incident: IncidentRecordType) {
  return (
    <>
      <IncidentViewHeader {...incident} />
      <IncidentBody {...incident} />
    </>
  )
}
