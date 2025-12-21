"use client"
import { useCallback } from "react"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "./SearchResults"
import Pagination from "./Pagination"
import Filter from "./Filter"
import { useSearch } from "@/providers/SearchProvider"

const PageResults = () => {
  const { searchResults, setPage, error } = useSearch()

  const handlePageChange = useCallback(
    (_event: unknown, value: number) => {
      setPage(value)
    },
    [setPage]
  )

  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter />
        <div className={styles.searchResultsWrapper}>
          <SearchBar />
          {error && (
            <div style={{ color: "red", padding: "1rem", textAlign: "center" }}>Error: {error}</div>
          )}
          <SearchResults
            total={searchResults?.total ?? 0}
            results={Array.isArray(searchResults?.results) ? searchResults.results : []}
          />
          <Pagination
            page={searchResults?.page}
            count={searchResults?.pages}
            onChangeHandler={handlePageChange}
          />
        </div>
      </section>
    </div>
  )
}

export default PageResults
