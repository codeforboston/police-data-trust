import {
  faGreaterThan,
  faPlusCircle,
  faSlidersH,
  IconDefinition
} from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"
import { TooltipIcons, TooltipTypes } from ".."
import { InfoTooltip } from "../../shared-components"

import styles from "../../shared-components/data-table/data-table.module.css"

// TODO: get API

export const resultsColumns = [
  {
    Header: "Officer(s) Involved",
    accessor: (row: any) => row["officers"].join(", "),
    id: "officers"
  },
  {
    Header: () => (
      <span className="columnHead">
        Date/Time
        <InfoTooltip type={TooltipTypes.DATETIME} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: (row: any) => new Date(row["occurred"]).toLocaleDateString(),
    id: "occurred"
  },
  {
    Header: "Incident Type",
    accessor: "incidentType"
  },
  {
    Header: () => (
      <span className="columnHead">
        Use of Force
        <InfoTooltip type={TooltipTypes.USEFORCE} icon={TooltipIcons.INFO} iconSize="xs" />
      </span>
    ),
    accessor: (row: any) => row["useOfForce"].join(", "),
    id: "useOfForce"
  },
  {
    Header: "Source",
    accessor: "source"
  },
  {
    Header: "Full",
    accessor: "full",
    Cell: () => {
      return (
        <FontAwesomeIcon
          className={styles.actionBtn}
          title={"Full"}
          icon={faGreaterThan}
          onClick={() => console.log("clicked")}
        />
      )
    },
    id: "full"
  },
  {
    Header: "Save",
    accessor: "save",
    Cell: () => {
      return (
        <FontAwesomeIcon
          className={styles.actionBtn}
          title={"Full"}
          icon={faPlusCircle}
          onClick={() => console.log("clicked")}
        />
      )
    },
    id: "save"
  },
  {
    Header: () => (
      <span className="columnHeadIcon">
        <FontAwesomeIcon icon={faSlidersH} size="lg" />
      </span>
    ),
    accessor: "id",
    disableSortBy: true
  }
]

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
