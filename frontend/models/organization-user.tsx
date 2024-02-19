import { Column } from "react-table"

enum MemberRole {
  ADMIN = "Administrator",
  PUBLISHER = "Publisher",
  MEMBER = "Member",
  SUBSCRIBER = "Subscriber",
  NONE = ""
}

enum ActionOptions {
  REMOVE = "Remove",
  WITHDRAW = "Withdraw",
  INVITATION = "Invitation"
}

enum Organizations {
  ORG1 = "Organization 1",
  ORG2 = "Organization 2",
  ORG3 = "Organization 3"
}

enum Users {
  USER1 = "User 1",
  USER2 = "User 2"
}

enum Status {
  PENDING = "Pending",
  CURRENT = "Current Member"
}

export interface CurrentOrgUsers {
  select: boolean
  user: string
  role: MemberRole
  status: Status
  action: string
  id: number
}

export const orgUsers: CurrentOrgUsers[] = [
  {
    select: false,
    user: "Angel Z",
    role: MemberRole.PUBLISHER,
    status: Status.PENDING,
    action: "",
    id: 0
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.PENDING,
    action: "",
    id: 1
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.CURRENT,
    action: "",
    id: 2
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.CURRENT,
    action: "",
    id: 3
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.CURRENT,
    action: "",
    id: 4
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.CURRENT,
    action: "",
    id: 5
  },
  {
    select: false,
    user: "",
    role: MemberRole.NONE,
    status: Status.CURRENT,
    action: "",
    id: 6
  }
]

export const actionOptions = [
  {
    item: ActionOptions.REMOVE,
    text: "Remove"
  },
  {
    item: ActionOptions.WITHDRAW,
    text: "Withdraw"
  },
  {
    item: ActionOptions.INVITATION,
    text: "Invitation"
  }
]

export const changeRoleOptions = [
  {
    item: MemberRole.ADMIN,
    text: "Admin"
  },
  {
    item: MemberRole.MEMBER,
    text: "Withdraw"
  },
  {
    item: MemberRole.PUBLISHER,
    text: "Publisher"
  },
  {
    item: MemberRole.SUBSCRIBER,
    text: "Subscriber"
  },
  {
    item: MemberRole.NONE,
    text: "None"
  }
]

export const organizationOptions = [
  {
    item: Organizations.ORG1,
    text: "Organization 1"
  },
  {
    item: Organizations.ORG2,
    text: "Organization 2"
  },
  {
    item: Organizations.ORG3,
    text: "Organization 3"
  }
]

export const userOptions = [
  {
    item: Users.USER1,
    text: "User 1"
  },
  {
    item: Users.USER2,
    text: "User 2"
  }
]
