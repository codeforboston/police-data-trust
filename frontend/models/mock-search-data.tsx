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

export const resultsData = [
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Dan Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Ed Smith, Vince Gilligan"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Dan Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Ed Smith, Vince Gilligan"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
  {
    searchDate: "2021/09/07",
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faAngleRight
  },
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
  },
]

export const searchesData = [
  {
    searchDate: "2021/09/07",
    who: ["Dillon, Matt"],
    what: "n/a",
    when: "n/a",
    where: "New York (state)",
    results: 124,
    view: faCaretRight
  }
]
