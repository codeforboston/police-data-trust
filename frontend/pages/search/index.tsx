import { Column } from "react-table"
import { DashboardHeader, Map, SearchPanel, SearchResultsTable } from "../../compositions"
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

export default requireAuth(function Dashboard() {
  const { searchPageContainer, searchPageDisplay } = styles
  const { incidentResults } = useSearch()
  const [toggleOptions, setToggleOptions] = useState(
    new ToggleOptions("incidents", "officers").options
  )

  return (
    <Layout>
      <div className={searchPageContainer}>
        <SearchPanel toggleOptions={toggleOptions} setToggleOptions={setToggleOptions} />
        <div className={searchPageDisplay}>
          <Map />
          {toggleOptions[0].value && !!incidentResults && (
            <SearchResultsTable
              results={incidentResults.results}
              resultsColumns={resultsColumns}
            />
          )}
          {toggleOptions[1].value && !!officerSearchResult && (
            <SearchResultsTable results={officerSearchResult} resultsColumns={officerResultsColumns} />
          )}
        </div>
      </div>
    </Layout>
  )
})

const officerSearchResult: Officer[] = [
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  },
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    race: "White",
    ethnicity: "Non-Hispanic",
    gender: "Male",
    rank: Rank.CAPTAIN,
    star: "123456",
    date_of_birth: new Date("01/01/1980")
  }
]
