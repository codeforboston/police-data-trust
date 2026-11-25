"use client"
import { useCallback } from "react"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "@/components/search/SearchResults"
import Pagination from "./Pagination"
import Filter from "./Filter"
import { hasActiveFilters, useSearch } from "@/providers/SearchProvider"

const PageResults = () => {
  const { searchResults, setPage, error, state } = useSearch()
  const results = Array.isArray(searchResults?.results) ? searchResults.results : []

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
          <SearchBar showLoginRequiredMessage />
          {error && (
            <div style={{ color: "red", padding: "1rem", textAlign: "center" }}>Error: {error}</div>
          )}
          <SearchResults
            tab={state.tab}
            total={searchResults?.total ?? 0}
            results={results}
            term={state.term}
            hasFilters={hasActiveFilters(state)}
            page={searchResults?.page ?? state.page}
            searched={searchResults !== undefined && !error}
          />
          {results.length > 0 && (
            <Pagination
              page={searchResults?.page}
              count={searchResults?.pages}
              onChangeHandler={handlePageChange}
            />
          )}
        </div>
      </section>
    </div>
  )
}

export default PageResults
