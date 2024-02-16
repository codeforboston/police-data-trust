import styles from "./profile-orguser.module.css"
import {DataTable} from "../../shared-components/data-table/data-table"
import {Column, CellProps, Cell, Row} from "react-table"
import { PrimaryButton } from "../../shared-components";
import Link from "next/link"
//import orgusers from "../../models/mock-data/orgusers"
import { ToggleBox } from "../../shared-components";
import ToggleDropDown from "../../shared-components/toggle-dropdown/toggle-dropdown";
import { useEffect, useState } from "react";

export enum MemberRole {
  ADMIN = "Administrator",
  PUBLISHER = "Publisher",
  MEMBER = "Member",
  SUBSCRIBER = "Subscriber",
  NONE = ""
}

export enum ActionOptions{
  REMOVE = "Remove",
  WITHDRAW = "Withdraw",
  INVITATION = "Invitation"
}

enum Status {
  PENDING = "Pending",
  CURRENT = "Current Member"
  
}

interface CurrentOrgUsers {
  select: boolean
  user: string
  role: MemberRole
  status: Status
  action: string
  id: number
}

export default function OrgUserTable(){
  //to show or not to show toggle button
  const[showToggle, setShowToggle] = useState<boolean>(false)
  //1. the useState to see if selected rows greater than 0
  //have to make this an array of selected Rows so that each of them can be edited
  const[selectedRows, setSelectedRows] = useState<number>(0)
  const[listOfRows, setListofRows] = useState<CurrentOrgUsers[]>([])


  function handleSelectRows(row: CurrentOrgUsers){
    row.select = !row.select;
    setSelectedRows(selectedRows + (row.select ? 1 : -1));

    setShowToggle(selectedRows > 0);
    
  }



  //Creating the mock data
  const orgUsers: CurrentOrgUsers[]= [
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
      status:Status.CURRENT,
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

  //Creating the columns
  const lawyerUserColumns: Column<CurrentOrgUsers>[] =[
    {
      Header: "Select",
      accessor: "select",
      Cell:({row}) =>{
        return <input type = "checkbox"
        onClick = {() =>{console.log("checked"); 
        row.original.select = true;
      }}
        onChange={() => handleSelectRows(row.original)}

        />
      },
      id: "select"
    },
    {
      Header: "User",
      accessor: "user",
      id: "user"
    },
    {
      Header: "Role",
      accessor: "role",
      id: "role"
    },
    {
      Header: "Status",
      accessor: "status",
      id: "status"
    },
    {
      Header: "Action",
      accessor: "action",
      id: "action"
    }
  ]


  const options = [
    "Org1",
    "Org2"
  ]

  const actionOptions = [
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
    },
  ]

  const changeRoleOptions = [
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

  return (

      <div className = {styles.container}>
        {showToggle &&
          <><ToggleDropDown title="Action" options={actionOptions} editChange={null} />
          <ToggleDropDown title="Change Roles" options={changeRoleOptions} editChange={null} /></>
        }
          <DataTable tableName ="Users" 
          columns = {lawyerUserColumns} 
          data = {orgUsers} />
          <Link href="../user-invite">
              <PrimaryButton className = {styles.invite_user} children = "Invite User"/>
          </Link>       
      </div>
  )
}