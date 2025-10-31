"use client"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "./SearchResults"
import Pagination from "./Pagination"
import Filter from "../../components/Filter/Filter"
import { useSearch } from "@/providers/SearchProvider"

// TODO: Hardcoded - obtain from sources
// TODO: Also obtain count from sources and switch options to FilterItems
const FILTER_GROUP_1 = {
  title: "Locations",
  filter: "location", // TODO: Handle from broader to narrower (can expand / dropdown)
  options: [{id: 0, title: "All locations", count: 10}, 
             {id: 1, title: "New York City", count: 6},
             {id: 2, title: "Texas State", count: 4}],
  withSearch: true
}

const FILTER_GROUP_2 = {
  title: "Data Sources",
  filter: "source", // Sources
  options: [{id: 0, title: "National Police Index", count: 30},
             {id: 1, title: "50-a.org", count: 20}],
  withSearch: true
}

const PageResults = ({}) => {
  const { searchResults } = useSearch()
  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter filters={[FILTER_GROUP_1, FILTER_GROUP_2]}/>
        <div className={styles.searchResultsWrapper}>
          <SearchBar />
          <SearchResults
            total={searchResults?.total ?? 0}
            results={Array.isArray(searchResults?.results) ? searchResults.results : []}
          />
          <Pagination
            page={searchResults?.page}
            count={searchResults?.pages}
            onChangeHandler={() => {}}
          />
        </div>
      </section>
    </div>
  )
}

export default PageResults
