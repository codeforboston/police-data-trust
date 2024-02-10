import styles from "./profile-orguser.module.css"
import {DataTable} from "../../shared-components/data-table/data-table"
import {Column, Row} from "react-table"
import { PrimaryButton } from "../../shared-components";
import Link from "next/link"
import orgusers from "../../models/mock-data/orgusers.json"
import { ToggleBox } from "../../shared-components";
import { ToggleDropDown } from "../../shared-components/toggle-dropdown/toggle-dropdown";
import { User } from '../../helpers/api';
import { Perpetrator, Incident } from '../../helpers/api';
import { useEffect, useState } from "react";
import { update } from "lodash";

export default function UserTable(){
  const data = orgusers
  const [selectedRows, updatedSelectedRows] = useState([])
  const [showToggles, setShowToggles] = useState(false)
  // const [isChecked, setIsChecked] = useState(false)
  // const [checboxes, setCheckboxes] = useState([])

  // useEffect(() => {
  //   setCheckboxes(data)
  // },[])

  // const handleCheckbox = (id) =>{
  //   const updatedCheckboxes = checkboxes.map((checkbox)=>
  //   )
  // }
  const handlerowsSelect = (row: Row<any>) =>{
    const rowIndex = selectedRows.findIndex(selectedRow => selectedRow.id === row.id)

    // setIsChecked(!isChecked)
    if(rowIndex === -1){
      updatedSelectedRows([...selectedRows,row])
    }else{
      const updatedRows =[...selectedRows];
      updatedRows.splice(rowIndex, 1);
      updatedSelectedRows(updatedRows)
    }

    setShowToggles(selectedRows.length>0)
  }
  const lawyerUserColumns: Column<any>[] = [
    {
        Header: "Select",
        accessor: "select",
        Cell: ({row}) =>{
            return <input type = "checkbox" 
            // checked = {isChecked} 
            onChange = {()=> handlerowsSelect(row)} />
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
      accessor: "Action",
      id: "Action"
    }
  
  ]

  const options = [
    "Org1",
    "Org2"
  ]

  const actionOptions = ["Remove", "Withdraw", "Invitation"]

  return (

      <div className = {styles.container}>
          <ToggleDropDown title = "Organizations" options = {options} />
          {showToggles && (
            
            <ToggleDropDown title = "Actions" options = {actionOptions}/>
            
            )}
          <DataTable tableName ="Users" 
          columns = {lawyerUserColumns} data = {data} />
          <Link href="../user-invite">
              <PrimaryButton className = {styles.invite_user} children = "Invite User"/>
          </Link>       
      </div>
  )
}