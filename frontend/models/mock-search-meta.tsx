import { faCaretRight, faAngleRight, IconDefinition } from "@fortawesome/free-solid-svg-icons"

export const resultsColumns = [
  {
    Header: "Search Date",
    accessor: "searchDate" as const
  },
  {
    Header: "Incident Date(s)",
    accessor: "dates" as const
  },
  {
    Header: "Incident Type",
    accessor: "incidentType" as const
  },
  {
    Header: "Officer(s)",
    accessor: "officersInvolved" as const
  },
  {
    Header: "Subject",
    accessor: "subject" as const
  },
  {
    Header: "Source",
    accessor: "source" as const
  },
  {
    Header: "View Record",
    accessor: "full" as const
  }
]

export const searchesColumns = [
  {
    Header: "Search Date",
    accessor: "searchDate" as const
  },
  {
    Header: "Who",
    accessor: "who" as const
  },
  {
    Header: "What",
    accessor: "what" as const
  },
  {
    Header: "When",
    accessor: "when" as const
  },
  {
    Header: "Where",
    accessor: "where" as const
  },
  {
    Header: "Results Total",
    accessor: "results" as const
  },
  {
    Header: "View Results",
    accessor: "view" as const
  }
]
