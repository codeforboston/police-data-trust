"use client"
import SearchBar from "@/components/SearchBar"
import styles from "./page.module.css"
import SearchResults from "./SearchResults"
import Pagintation from "./Pagination"
import Filter from "./Filter"

export type SearchResult = {
  id: string | number
  title: string
  subtitle: string
  description?: string
  tags: string[]
}

const RESULTS: SearchResult[] = [
  {
    id: 1,
    title: "Amada A defds",
    subtitle: "Asian man, Detective Grade 3 at Criminal Intelligence Section, New York",
    tags: ["Officer", "50-a.org", "Last updated on Nov 21, 2024"]
  },
  {
    id: 2,
    title: "Property Damaged",
    subtitle: "Closed, #202100486, December 15, 2020, New York",
    tags: ["Complaint", "50-a.org", "Last updated on Nov 21, 2024"]
  },
  {
    id: 3,
    title: "New York City Police Department",
    subtitle: "New York",
    tags: ["Unit", "50-a.org", "Last updated on Nov 21, 2024"]
  }
]

const PageResults = ({}) => {
  return (
    <div className={styles.wrapper}>
      <section className={styles.searchWrapper}>
        <Filter />
        <div className={styles.searchResultsWrapper}>
          <SearchBar />
          <SearchResults results={RESULTS} />
          <Pagintation page={0} count={7} onChangeHandler={() => {}} />
        </div>
      </section>
    </div>
  )
}

export default PageResults
