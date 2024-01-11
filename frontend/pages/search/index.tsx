import { useState } from "react"
import { requireAuth, useSearch } from "../../helpers"
import { Officer, Rank } from "../../helpers/api"
import { ToggleOptions } from "../../models"
import { Layout } from "../../shared-components"
import { SearchForm } from "./search-page-components/search-form"
import { SearchResults } from "./search-page-components/search-results"
import styles from "./search.module.css"

export default requireAuth(function SearchPage() {
  const { searchPageContainer } = styles
  const { incidentResults } = useSearch()
  const [toggleOptions, setToggleOptions] = useState(
    new ToggleOptions("incidents", "officers").options
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
