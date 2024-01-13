import { useMediaQuery } from "react-responsive"
import { BubbleChart, Map, SearchResultsTable } from "../../../compositions"
import { resultsColumns } from "../../../compositions/search-results/search-results"
import { IncidentSearchResponse, Officer } from "../../../helpers/api"
import { IToggleOptions } from "../../../models"
import { createOfficerColumns } from "../../../models/officer"
import styles from "./search-results.module.css"

interface SearchResultsProps {
  toggleOptions: IToggleOptions[]
  incidentResults: IncidentSearchResponse
  officerSearchResult: Officer[]
}

export function SearchResults({
  toggleOptions,
  incidentResults,
  officerSearchResult
}: SearchResultsProps) {
  const { searchResultsContainer, searchResultsHeader } = styles
  const isIncidentView = toggleOptions[0].value
  const isOfficerView = toggleOptions[1].value
  const desktop = useMediaQuery({ query: "screen and (min-width: 70em)" })
  const allegationFullLength = useMediaQuery({ query: "(min-width: 32em)" })

  const hasIncidentResults = !!incidentResults
  const hasOfficerResults = !!officerSearchResult

  return (
    <section className={searchResultsContainer}>
      {/* INCIDENT VIEW */}
      {!desktop && isIncidentView && hasIncidentResults && (
        <h2 className={searchResultsHeader}>Incident Results</h2>
      )}
      {isIncidentView && !hasIncidentResults && (
        <h2 className={searchResultsHeader}>Search for incidents in the database.</h2>
      )}
      {desktop && isIncidentView && <Map />}
      {isIncidentView && hasIncidentResults && (
        <SearchResultsTable results={incidentResults.results} resultsColumns={resultsColumns} />
      )}

      {/* OFFICER VIEW */}
      {!desktop && isOfficerView && hasOfficerResults && (
        <h2 className={searchResultsHeader}>Officer Results</h2>
      )}
      {isOfficerView && !hasOfficerResults && (
        <h2 className={searchResultsHeader}>Search for officers in the database.</h2>
      )}
      {desktop && isOfficerView && <BubbleChart height={325} />}
      {isOfficerView && hasOfficerResults && (
        <SearchResultsTable
          results={officerSearchResult}
          resultsColumns={createOfficerColumns(allegationFullLength)}
        />
      )}
    </section>
  )
}
