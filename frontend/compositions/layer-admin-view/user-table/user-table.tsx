import styles from './user-table.module.css';
import {Column} from "react-table"
import { DataTable } from '../../../shared-components/data-table/data-table';
import { User } from '../../../helpers/api';
import { Perpetrator, Incident } from '../../../helpers/api';

export const lawyerUserColumns: Column<any>[] = [
    {
        Header: "Select",
        accessor: "select",
        Cell: () =>{
            return <input type = "checkbox" onClick = {() => console.log("checked")} />
        },
        id: "select"  
    },
    {
        Header: "Name",
        accessor: (row: any) =>
            row["lawyers"].map((names: User) => Object.values(names).join(", ")).join(", "),
        id: "lawyers"
    }

]
export default function UserTable(results: Incident[]){
    return(
        <>
        <DataTable tableName='Lawyer Members' columns={lawyerUserColumns} data = {results}/>
        </>
    )
}




// interface UserTable {
//     data: Array<{ name: string; role: string; status: "Pending" | "Current Member" }>;
// }

// export default function UserTable(userTableProps: UserTableProps){

//   const { users, usersColumns} = userTableProps

//   return (
   
//     <>
//         {!!userTableProps.users?.length? (
      
//             <DataTable tableName={'Current Organization Members'} columns = {usersColumns} data = {users} />
//         ) : (
//             <DataTable tableName = {'Current Organization Members'} columns = {usersColumns} data = {users ?? Array(8).fill({})}/>
//         )};
//     </>
//   );
// };

// export const usersColumns: Column<any>[]  =[
//     {
//         Header: " ",
//         accessor: "select",
//         Cell: () =>{
//             return <input type = "checkbox" onClick = {() => console.log("checked")} />
//         },
//         id: "select"
//     },
//     {
//         Header: "Name", 
//         accessor: (row: any) =>
//             row["username"].map((usernames: UserTableProps ) => Object.values(usernames).join(", ")).join(", "),
//         filter: "text",
//         id: "username"
//     }
// ]
