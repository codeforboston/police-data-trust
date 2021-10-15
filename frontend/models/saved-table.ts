// SAVED RESULTS DATA TABLE
export interface SavedResultsType {
  searchDate: number // UNIX timestamp
  id: number
  occurred: number // UNIX timestamp
  officers: string[] // officer names, "F.Last" (first initial, last name)
  incidentType: string
  useOfForce: string[]
  source: string
}

export const resultsColumns = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Date/Time",
    accessor: (row: any) => formatDate(row["occurred"]),
    id: "occurred"
  },
  {
    Header: "Officer(s)",
    accessor: (row: any) => row["officers"].join(", "),
    id: "officers"
  },
  {
    Header: "Incident Type",
    accessor: "incidentType"
  },
  {
    Header: "Use of Force",
    accessor: (row: any) => row["useOfForce"].join(", "),
    id: "useOfForce"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "View",
    accessor: "id",
    disableSortBy: true
  }
]

const formatDate = (unixDate: number): string => new Date(unixDate).toLocaleDateString()

// SAVED SEARCHES DATA TABLE
export interface SavedSearchType {
  searchDate: number // UNIX timestamp
  who: string[]
  what: string
  when: number // UNIX timestamp
  where: string
  total: number
  results: number
}


export const searchesColumns = [
  {
    Header: "Search Date",
    accessor: (row: any) => formatDate(row["searchDate"]),
    id: "searchDate"
  },
  {
    Header: "Who",
    accessor: (row: any) => row["who"].join(", "),
    id: "who"
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
    accessor: "results",
    disableSortBy: true
  }
]
