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

const PageResults = ({}) => {
  const { searchResults } = useSearch()
  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter />
        <div className={styles.searchResultsWrapper}>
          <SearchBar />
          <SearchResults results={Array.isArray(searchResults) ? searchResults : []} />
          <Pagintation page={0} count={7} onChangeHandler={() => {}} />
        </div>
      </section>
    </div>
  )
}

export default PageResults
