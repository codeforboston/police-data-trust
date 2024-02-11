import { CreateOrganizationBtn, DataTable } from "../../shared-components"
import styles from "./profile-notifications.module.css"

enum MemberRole {
  ADMIN = "Administrator",
  PUBLISHER = "Publisher",
  MEMBER = "Member",
  SUBSCRIBER = "Subscriber"
}

interface InterimInvitation {
  organization: string
  role: MemberRole
  dateInvited: Date
  status: string
}

export default function ProfileNotifications() {
  const { notificationsContainer, headerContainer, headerText, headerCTA } = styles

  // TODO: get user's invitations

  return (
    <section className={notificationsContainer}>
      <div className={headerContainer}>
        <h1 className={headerText}>Notifications</h1>
        <CreateOrganizationBtn btnClassName={headerCTA} />
      </div>
      <DataTable tableName="Notifications" data={notifications} columns={notificationsColumns} />
    </section>
  )
}

const notifications: InterimInvitation[] = [
  {
    organization: "Pearson Hardman",
    role: MemberRole.ADMIN,
    dateInvited: new Date("8/8/2021"),
    status: "Invitation"
  },
  {
    organization: "Pearson Hardman Litt",
    role: MemberRole.ADMIN,
    dateInvited: new Date("7/30/2021"),
    status: "Invitation"
  },
  {
    organization: "Zane Specter Litt",
    role: MemberRole.PUBLISHER,
    dateInvited: new Date("6/15/2021"),
    status: "Current Member"
  },
  {
    organization: "Porter Hedges",
    role: MemberRole.MEMBER,
    dateInvited: new Date("5/2/2021"),
    status: "Current Member"
  }
]

const notificationsColumns: Column<InterimInvitation>[] = [
  {
    Header: "Organization",
    accessor: "organization",
    id: "organization"
  },
  {
    Header: "Role",
    accessor: "role",
    id: "role"
  },
  {
    Header: "Date Invited",
    Cell: (props) => (
      <div>
        {new Intl.DateTimeFormat("en-US", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit"
        }).format(props.cell.value)}
      </div>
    ),
    accessor: "dateInvited",
    id: "dateInvited"
  },
  {
    Header: "Status",
    accessor: "status",
    id: "status"
  },
  {
    Header: "Action",
    Cell: () => (
      <PrimaryButton
        className={styles.actionBtn}
        onClick={() => console.log("join/leave clicked.")}>
        Join
      </PrimaryButton>
    )
  }
]
