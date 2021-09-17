export interface SavedResultsType {
  searchDate: Date,
  incidentDates: Date[],
  incidentType: string,
  offiersInvolved: string[],
  subject: string,
  source: string,
  fullRecordId: number
}

export interface DataColumn {
  Header: string,
  accessor: string
}

export interface DataColumns {
  columns: DataColumn[]
}

export interface SavedDataType {
  searchDate: Date,
  fullRecordId: number
}

export const resultsColumns = [
  {
    Header: "Search Date",
    accessor: "searchDate"
  },
  {
    Header: "Incident Date(s)",
    accessor: "dates"
  },
  {
    Header: "Incident Type",
    accessor: "incidentType"
  },
  {
    Header: "Officer(s)",
    accessor: "officersInvolved"
  },
  {
    Header: "Subject",
    accessor: "subject"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "View Record",
    accessor: "recordId"
  }
]

export interface SavedSearchType {
  searchDate: Date,
  who: string[],
  what: string,
  when: Date[],
  where: string,
  resultsCount: number,
  view: number
}

export const searchesColumns = [
  {
    Header: "Search Date",
    accessor: "searchDate"
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
    accessor: "when"
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
