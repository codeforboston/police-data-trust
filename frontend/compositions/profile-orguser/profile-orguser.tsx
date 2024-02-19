import styles from "./profile-orguser.module.css"
import {DataTable} from "../../shared-components/data-table/data-table"
import {Column} from "react-table"
import ToggleDropDown from "../../shared-components/toggle-dropdown/toggle-dropdown";
import { useState } from "react";
import InviteUserBtn from "./invite-user/invite-user-btn";
import { orgUsers, CurrentOrgUsers,actionOptions, changeRoleOptions, organizationOptions, userOptions } from "../../models/organization-user";


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
      </div>
  )
}