import OfficerHeader from "./officer-view-header"
import OptionalOfficerInfo from "./optional-officer-info"
import OfficerWorkHistory from "./officer-work-history"
import OfficerAffiliations from "./officer-affiliations"
import { OfficerRecordType } from "../../models/officer"
import styles from "./officer-view.module.css"
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useRouter } from "next/router"
import { OfficerIncidentDataTable } from "../../shared-components/officer-incident-data-table/officer-incident-data-table"
import { incidentResultsColumns } from "../../models/incident"

export default function OfficerView(officer: OfficerRecordType) {
  const { officerView, profilePicture, officerViewHeader, wrapper, backButton } = styles
  const router = useRouter()

  const BackButton = () => {
    return (
      <FontAwesomeIcon
        className={backButton}
        title={"Back"}
        icon={faArrowLeft}
        size="lg"
        onClick={() => router.back()}
      />
    )
  }

  return (
    <div className={wrapper}>
      <BackButton />
      <div className={officerView}>
        <img
          className={profilePicture}
          src={
            "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"
          }
          alt="Profile Picture"
        />
        <div>
          <OfficerHeader {...officer} />
          <OptionalOfficerInfo {...officer} />
          <OfficerWorkHistory {...officer} />
          {officer.incidents && officer.incidents.length > 0 && (
            <OfficerIncidentDataTable
              tableName=""
              columns={incidentResultsColumns}
              data={officer.incidents}
            />
          )}
        </div>
      </div>
    </div>
  )
}
