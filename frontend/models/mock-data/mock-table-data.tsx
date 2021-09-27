import { faGreaterThan, faPlusCircle, IconDefinition } from "@fortawesome/free-solid-svg-icons"

export const mockData = [
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Dan Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Ed Smith, Vince Gilligan"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Dan Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["Ed Smith, Vince Gilligan"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  },
  {
    dates: "2003/01/01",
    incidentType: "Use of force",
    officersInvolved: ["John Smith"],
    subject: "unknown",
    source: "News Article",
    full: faGreaterThan,
    save: faPlusCircle
  }
]

export const tableColumns = [
  {
    Header: "Date(s)",
    accessor: "dates" as const
  },
  {
    Header: "Incident Type",
    accessor: "incidentType" as const
  },
  {
    Header: "Officer(s) Involved",
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
    Header: "Full Record",
    accessor: "full" as const
  },
  {
    Header: "Save Record",
    accessor: "save" as const
  }
]
