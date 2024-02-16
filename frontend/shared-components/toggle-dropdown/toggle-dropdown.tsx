import React, {FC, useState} from "react";
import styles from "./toggle-dropdown.module.css"
import { MemberRole } from "../../compositions/profile-orguser/profile-orguser";
import { ActionOptions } from "../../compositions/profile-orguser/profile-orguser";


// enum ActionOptions{
//     REMOVE = "Remove",
//     WITHDRAW = "Withdraw",
//     INVITATION = "Invitation"
// }

// enum MemberRole {
//     ADMIN = "Administrator",
//     PUBLISHER = "Publisher",
//     MEMBER = "Member",
//     SUBSCRIBER = "Subscriber",
//     NONE = ""
//   }

interface ToggleDropDownProps{
    title: string,
    //item: ActionOptions | MemberRole,
    editChange: Function
    options: any[]

}

export default function ToggleDropDown({title, editChange, options}: ToggleDropDownProps) {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropDown = () =>{
        setIsOpen(!isOpen)
    }
    return(
        <div className = {styles.togglebutton}>
            <button onClick={toggleDropDown}>{title}</button>
            {isOpen && (
                <div className = {styles.popup}>
                    <ul>
                        {options.map((option)=>(
                            <li key = {option.item} onClick = {() => editChange(option.item)}>
                                {option.text}
                            </li>
                        ))}

                    </ul>
                </div>  
            )}

        </div>
    )
}


