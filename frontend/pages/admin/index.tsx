import React, { FormEvent, useState } from "react"
import OrgUserTable from "../../compositions/profile-orguser/profile-orguser";




export default function LawyerAdmin() {
  return (     

    <div >
        
        {/* <SideMenu /> */}
        <OrgUserTable/>
        {/* <DataTable tableName="Users" columns={lawyerUserColumns} data = {data}/> */}

    </div>
  );
}


