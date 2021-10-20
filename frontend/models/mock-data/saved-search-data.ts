// SAVED SEARCH DATA TABLE
export interface SavedSearchType {
  searchDate: number // UNIX timestamp
  who: string[]
  what: string
  when: number // UNIX timestamp
  where: string
  total: number
  results: number
}

const formatDate = (unixDate: number): string => new Date(unixDate).toLocaleDateString()

export const searchesColumns = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Who",
    accessor: "who"
  },
  {
    Header: "What",
    accessor: "what"
  },
  {
    Header: "When",
    accessor: (row: any) => formatDate(row["when"]),
    id: "when"
  },
  {
    Header: "Where",
    accessor: "where"
  },
  {
    Header: "Results Total",
    accessor: "total"
  },
  {
    Header: "View Results",
    accessor: "results"
  }
]

export const savedSearchData = [
  {
    searchDate: 1581007526000,
    who: ["M.Dillon"],
    what: "n/a",
    when: 1482251257000,
    where: "New York (state)",
    total: 124,
    results: 1
  },
  {
    searchDate: 1611321729000,
    who: ["n/a"],
    what: "Use of Force",
    when: 1302852303000,
    where: "Chicago, Illinois",
    total: 1200,
    results: 2
  }
]
