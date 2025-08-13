"use client"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "./SearchResults"
import Pagination from "./Pagination"
import Filter from "./Filter"
import { useSearch } from "@/providers/SearchProvider"

const PageResults = ({}) => {
  const { searchResults } = useSearch()
  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter />
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
