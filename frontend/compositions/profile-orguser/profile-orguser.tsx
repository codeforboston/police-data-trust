import styles from "./profile-orguser.module.css"
import {DataTable} from "../../shared-components/data-table/data-table"
import {Column} from "react-table"
import ToggleDropDown from "../../shared-components/toggle-dropdown/toggle-dropdown";
import { useState } from "react";
import InviteUserBtn from "./invite-user-btn";


enum MemberRole {
  ADMIN = "Administrator",
  PUBLISHER = "Publisher",
  MEMBER = "Member",
  SUBSCRIBER = "Subscriber",
  NONE = ""
}

enum ActionOptions{
  REMOVE = "Remove",
  WITHDRAW = "Withdraw",
  INVITATION = "Invitation"
}

enum Organizations{
  ORG1 = "Organization 1",
  ORG2 = "Organization 2",
  ORG3 = "Organization 3"
}

enum Users{
  USER1 = "User 1",
  USER2 = "User 2"
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

  const[selectedRowsId, setSelectedRowsId] = useState<CurrentOrgUsers["id"][]>([])

  function handleSelected(id: CurrentOrgUsers["id"]){

    if(selectedRowsId.includes(id)){
      setSelectedRowsId(selectedRowsId.filter(rowId => rowId !== id))
      if(selectedRowsId.length === 1){
        setShowToggle(false)
      }
    }else{
      setSelectedRowsId([...selectedRowsId,id])
      setShowToggle(true)
      
    }

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
        return <input 
        type = "checkbox"
        checked = {selectedRowsId.includes(row.original.id)}
        onChange={() => handleSelected(row.original.id)}
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

  const organizationOptions = [
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

  const userOptions = [
    {
      item: Users.USER1,
      text: "User 1"
    },
    {
      item: Users.USER2,
      text: "User 2"
    }
  ]

  return (

      <div className = {styles.container}>

        <div className = {styles.header}>

        </div>
          <div className = {styles.buttonrow}>
            <div className = {styles.buttonrow1}>
              <ToggleDropDown className = {styles.visiblebtn} title ="Organizations" options = {organizationOptions} editChange={null}/>
              <ToggleDropDown className = {styles.visiblebtn} title = "Users" options = {userOptions} editChange={null}/>
              

            </div>
            <div className ={styles.buttonrow2}>
              {showToggle &&
                  <><ToggleDropDown className = {styles.invisiblebtn} title="Action" options={actionOptions} editChange={null} />
                  <ToggleDropDown className = {styles.invisiblebtn} title="Change Roles" options={changeRoleOptions} editChange={null} /></>
                }
                
              <InviteUserBtn btnClassName={styles.invitebtn}/>
            </div>
          </div>
          <div className = {styles.table}>
            <DataTable tableName ="Users" columns = {lawyerUserColumns} data = {orgUsers} />
          </div>
          {/* <p>{Object.keys(selectedRowsId)}</p> 
          <p>{Object.keys(selectedRowsId).length}</p>       */}
      </div>
  )
}