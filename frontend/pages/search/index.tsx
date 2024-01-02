import { Column } from "react-table"
import {
  BubbleChart,
  DashboardHeader,
  Map,
  SearchPanel,
  SearchResultsTable
} from "../../compositions"
import { resultsColumns } from "../../compositions/search-results/search-results"
import { requireAuth, useSearch } from "../../helpers"
import { Officer, Rank } from "../../helpers/api"
import { Layout } from "../../shared-components"
import styles from "./search.module.css"
import { CirclePlusButton } from "../../shared-components/icon-buttons/icon-buttons"
import ErrorAlertDialog from "../../shared-components/error-alert-dialog/error-alert-dialog"
import { useState } from "react"
import { officerResultsColumns } from "../../models/officer"
import { SearchResultsTypes, ToggleOptions } from "../../models"
import { mockToOfficerType } from "../../helpers/mock-to-officer-type"
import officer from "../../models/mock-data/officer.json"

export default requireAuth(function Dashboard() {
  const { searchPageContainer } = styles
  const { incidentResults } = useSearch()
  const [toggleOptions, setToggleOptions] = useState(
    new ToggleOptions("incidents", "officers").options
  )

  const isIncidentView = toggleOptions[0].value
  const isOfficerView = toggleOptions[1].value

  const officerSearchResult = Array.from({ length: 100 }, (_, index) =>
    mockToOfficerType(officer[index])
  )

  return (
    <Layout>
      <div className={searchPageContainer}>
        <SearchPanel toggleOptions={toggleOptions} setToggleOptions={setToggleOptions} />
        <div>
          {isIncidentView && <Map />}
          {isIncidentView && !!incidentResults && (
            <SearchResultsTable results={incidentResults.results} resultsColumns={resultsColumns} />
          )}

          {isOfficerView && <BubbleChart height={325} />}
          {isOfficerView && !!officerSearchResult && (
            <SearchResultsTable
              results={officerSearchResult}
              resultsColumns={officerResultsColumns}
            />
          )}
        </div>
      </div>
    </Layout>
  )
})
