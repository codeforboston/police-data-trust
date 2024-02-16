import { useState } from "react"
import { SearchForm } from "../../compositions/search-page-components/search-form"
import { SearchResults } from "../../compositions/search-page-components/search-results"
import { requireAuth, useSearch } from "../../helpers"
import { mockToOfficerType } from "../../helpers/mock-to-officer-type"
import { ToggleOptions } from "../../models"
import officer from "../../models/mock-data/officer.json"
import { Layout } from "../../shared-components"
import styles from "./search.module.css"

export default requireAuth(function SearchPage() {
  const { searchPageContainer } = styles
  const { incidentResults } = useSearch()
  const [toggleOptions, setToggleOptions] = useState(
    new ToggleOptions("incidents", "officers").options
  )

  const officerSearchResult = Array.from({ length: 100 }, (_, index) =>
    mockToOfficerType(officer[index])
  )

  return (
    <Layout>
      <div className={searchPageContainer}>
        <SearchForm toggleOptions={toggleOptions} setToggleOptions={setToggleOptions} />
        <SearchResults
          toggleOptions={toggleOptions}
          incidentResults={incidentResults}
          officerSearchResult={officerSearchResult}
        />
      </div>
    </Layout>
  )
})
