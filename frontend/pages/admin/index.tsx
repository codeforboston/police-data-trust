import React, { FormEvent, useState } from "react"
import SideMenu from "../../compositions/layer-admin-view/side-menu/side-menu";
import UserTable from "../../compositions/layer-admin-view/user-table/user-table";
import styles from "./admin.module.css"
import { PrimaryButton } from "../../shared-components";
import Link from "next/link";


export default function LawyerAdmin() {
  return (     
    <div className= {styles.container}>
        
        <SideMenu />
        {/* <UserTable />  */}
        <Link href="../user-invite">
            <PrimaryButton className = {styles.invite_user} children = "Invite User"/>
        </Link>
    </div>
  );
}


