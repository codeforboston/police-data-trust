"use client"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "./SearchResults"
import Pagintation from "./Pagination"
import Filter from "./Filter"
import { useSearch } from "@/providers/SearchProvider"

export type SearchResult = {
  uid: string | number
  title: string
  subtitle: string
  content_type: string
  source: string
  last_updated: string
  description?: string
  tags?: string[]
}

export type PaginatedSearchResults = {
  page: number
  pages: number
  per_page: number
  total: number
  results: SearchResult[]
}

const PageResults = ({}) => {
  const { searchResults } = useSearch()
  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter />
        <div className={styles.searchResultsWrapper}>
          <SearchBar />
          <SearchResults
            total={searchResults.total}
            results={Array.isArray(searchResults?.results) ? searchResults.results : []}
          />
          <Pagintation
            page={searchResults.page}
            count={searchResults.pages}
            onChangeHandler={() => {}}
          />
        </div>
      </section>
    </div>
  )
}

export default PageResults
