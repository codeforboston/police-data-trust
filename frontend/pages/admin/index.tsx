import React, { FormEvent, useState } from "react"
import {
  ProfileInfo,
  ProfileNav,
  ProfileType,
  SavedResults,
  SavedSearches
} from "../../compositions"
import OrgUserTable from "../../compositions/profile-orguser/profile-orguser";
import styles from "../../compositions/profile-orguser/profile-orguser.module.css"
import { PrimaryButton } from "../../shared-components";
import Link from "next/link";
import { ProfileMenu } from "../../models/profile";
import { requireAuth } from "../../helpers";
import { DataTable } from "../../shared-components/data-table/data-table";
import { Column } from "react-table";



export default function LawyerAdmin() {
  return (     
    // const [activePage, setActivePage] = React.useState(ProfileMenu.ORGANIZATIONS) 

    // const ActivePageComp= (function (menuItem:ProfileMenu)){
    //   switch (menuItem) {
    //     case ProfileMenu.USER_INFO:
    //       return ProfileInfo
    //     case ProfileMenu.PROFILE_TYPE:
    //       return ProfileType
    //     case ProfileMenu.SAVED_RESULTS:
    //       return SavedResults
    //     case ProfileMenu.SAVED_SEARCHES:
    //       return SavedSearches
    //     case ProfileMenu.NOTIFICATIONS:
    //       return ProfileNotifications
    //     case ProfileMenu.ORGANIZATIONS:
    //       return ProfileOrganizations
    //     default:
    //       throw new Error("Must be a key in 'ProfileMenu' enum - unexpected default case!")
    // }
    // })(activepage)

    <div >
        
        {/* <SideMenu /> */}
        <OrgUserTable/>
        {/* <DataTable tableName="Users" columns={lawyerUserColumns} data = {data}/> */}

    </div>
  );
}


