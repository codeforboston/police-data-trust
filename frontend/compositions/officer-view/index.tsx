import OfficerHeader from "./officer-view-header"
import OptionalOfficerInfo from "./optional-officer-info"
import OfficerWorkHistory from "./officer-work-history"
import OfficerAffiliations from "./officer-affiliations"
import { OfficerRecordType } from "../../models/officer"
import { DataTable } from "../../shared-components/data-table/data-table"
import { resultsColumns } from "../search-results/search-results"
import { EXISTING_TEST_INCIDENTS } from "../../helpers/api/mocks/data"

export default function OfficerView(officer: OfficerRecordType) {
  return (
    <>
      <OfficerHeader {...officer} />
      <hr />
      <OptionalOfficerInfo {...officer} />
      <hr />
      <OfficerWorkHistory {...officer} />
      <OfficerAffiliations {...officer} />
      {/* TODO: <DataTable tableName='Mock Table' columns={resultsColumns} data={EXISTING_TEST_INCIDENTS} /> */}
    </>
  )
}
